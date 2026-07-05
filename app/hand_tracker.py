import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


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

                count = 0

                if index_up:
                    count += 1

                if middle_up:
                    count += 1

                if ring_up:
                    count += 1

                if pinky_up:
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
                
                if count == 4:
                    gesture = "OPEN PALM"
                elif count == 0:
                    gesture = "FIST"    
                elif (
                    not ring_up and
                    not pinky_up and
                    middle_up and
                    index_up
                ): gesture = "PEACE"
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
                    
                    
                        
                    
        
        
        

        # print(result.hand_landmarks)

        cv2.imshow("gesture stage Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    landmarker.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
