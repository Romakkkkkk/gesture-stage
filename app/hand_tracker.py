import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time 


def main():

    model_path = "models/hand_landmarker.task"
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=2,
        min_hand_detection_confidence=0.3,
        min_hand_presence_confidence=0.3,
        min_tracking_confidence=0.3,
    )

    landmarker = vision.HandLandmarker.create_from_options(options)

    cap = cv2.VideoCapture(0)
    
    last_action_time = 0
    cooldown_time = 1.0
    current_effect = "NONE"

    while True:
        success, frame = cap.read()

        if not success:
            print("failed to read from webcam")
            break

        frame = cv2.flip(frame, 1)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        result = landmarker.detect(mp_image)

        if result.hand_landmarks:
            for hand_index, hand_landmarks in enumerate(result.hand_landmarks):
                handedness = result.handedness[hand_index][0].category_name
                h, w, _ = frame.shape
                for i, landmark in enumerate(hand_landmarks):

                    x = int(landmark.x * w)
                    y = int(landmark.y * h)

                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

                    cv2.putText(
                        frame,
                        str(i),
                        (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255, 255, 255),
                        1,
                    )
                index_up = hand_landmarks[8].y < hand_landmarks[6].y
                middle_up = hand_landmarks[12].y < hand_landmarks[10].y
                ring_up = hand_landmarks[16].y < hand_landmarks[14].y
                pinky_up = hand_landmarks[20].y < hand_landmarks[18].y
                
                if handedness == "Right":
                    thumb_up = hand_landmarks[4].x > hand_landmarks[3].x
                else:
                    thumb_up = hand_landmarks[4].x < hand_landmarks[3].x
                    
                count = 0

                if index_up:
                    count += 1

                if middle_up:
                    count += 1

                if ring_up:
                    count += 1

                if pinky_up:
                    count += 1
                    
                if thumb_up:
                    count += 1
                        

                text_y = 50 + (hand_index * 40)


                cv2.putText(
                    frame,
                    f"{handedness}: {count}",
                    (20, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )     
                
                if count == 5:
                    gesture = "OPEN PALM"
                elif count == 0:
                    gesture = "FIST"    
                elif (
                    not ring_up and
                    not pinky_up and
                    middle_up and
                    index_up
                ): gesture = "PEACE"
                elif thumb_up and count == 1:
                    gesture = "THUMBS UP"
                elif index_up and pinky_up and count == 2:
                    gesture = "ROCK"
                elif index_up and count == 1:
                    gesture = "POINT"        
                else:
                    gesture = "UNKNOWN"
                
                text_x = int(hand_landmarks[0].x * w)
                text_y = int(hand_landmarks[0].y * h) - 30
                
                text_x = max(10, min(text_x, w - 200))
                text_y = max(40, min(text_y, h - 20))

                cv2.putText(
                    frame,
                    gesture,
                    (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )
                cv2.putText(
                    frame,
                    f"Hands detected: {len(result.hand_landmarks)}",
                    (20, 130),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    2,
                )
                current_time = time.time()

                if current_time - last_action_time >= cooldown_time:
                    if gesture == "OPEN PALM":
                        current_effect = "NORMAL"
                    elif gesture == "FIST":
                        current_effect = "FREEZE"
                    elif gesture == "PEACE":
                        current_effect = "PARTY MODE"
                    elif gesture == "THUMBS UP":
                        current_effect = "APPROVED"
                    elif gesture == "ROCK":
                        current_effect = "EDGE"
                    elif gesture == "POINT":
                        current_effect = "GRAYSCALE"

                    last_action_time = current_time

                cv2.putText(
                    frame,
                    f"Effect: {current_effect}",
                    (20, 180),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 255),
                    2,
                )   

                if current_effect == "NORMAL":
                    pass
                elif current_effect == "PARTY MODE":
                    frame = cv2.bitwise_not(frame)
                elif current_effect == "EDGE":
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray, 100, 200)
                    frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)   
                elif current_effect == "GRAYSCALE":     
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
                
                    
                
        # print(result.hand_landmarks)

        cv2.imshow("gesture stage Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    landmarker.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
