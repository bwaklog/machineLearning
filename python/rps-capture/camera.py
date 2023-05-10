import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False,
                         min_detection_confidence=0.5,
                         min_tracking_confidence=0.5)

vid = cv2.VideoCapture(0)

while True:
    ret, frame = vid.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame)

    result_pose = pose.process(frame)

    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame,
                                                  hand_landmark,
                                                  mp_hands.HAND_CONNECTIONS)
            
            fingers = []
            for id, landmark in enumerate(hand_landmark.landmark):
                if landmark.y < hand_landmark.landmark[mp_hands.HandLandmark.WRIST].y:
                    if id < 5:
                        fingers.append(0)
                    elif id < 9:
                        fingers.append(1)
                    elif id < 13:
                        fingers.append(2)
                    elif id < 17:
                        fingers.append(3)
                if len(fingers) == 5:
                    if fingers == [0, 1, 4, 4, 3]:
                        gesture = 'rock'
                    elif fingers == [2, 0, 3, 3, 3]:
                        gesture = 'paper'
                    elif fingers == [2, 0, 1, 1, 1]:
                        gesture = 'scissors'

                else:
                    gesture = 'unknown'

                cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Hand Detection', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    if cv2.waitKey(1) == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()