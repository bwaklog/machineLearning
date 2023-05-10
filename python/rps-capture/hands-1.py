import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_style = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def getHandMove(hand_landmarks):
    landmarks = hand_landmarks.landmark
    if all(landmarks[i].y < landmarks[i+3].y for i in range(9, 20, 4)):
        return 'rock'
    elif landmarks[13].y < landmarks[16].y and landmarks[17].y < landmarks[20].y:
        return 'scissors'
    else:
        return 'paper'
    

vid = cv2.VideoCapture(0)

clock = 0
p1_move = p2_move = None
gameText = ""
sucess = True

with mp_hands.Hands(model_complexity=0,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as hands:
    
    while True:
        ret, frame = vid.read()
        if not ret or frame is None:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame,
                                          hand_landmarks,
                                          mp_hands.HAND_CONNECTIONS,
                                          mp_drawing_style.get_default_hand_landmarks_style(),
                                          mp_drawing_style.get_default_hand_connections_style())
                
        frame = cv2.flip(frame, 1)

        if 0 <= clock < 20:
            sucess = True
            gameText = "Ready?"

        elif clock < 30:
            gameText="3..."
        elif clock < 40:
            gameText="2..."
        elif clock < 50:
            gameText="1..."
        elif clock < 60:
            gameText="GO!"
        elif clock == 60:
            hls = results.multi_hand_landmarks
            if hls and len(hls) ==2:
                p1_move = getHandMove(hls[0])
                p2_move = getHandMove(hls[1])
            else:
                sucess=False

        elif clock < 100:
            if sucess:
                gameText = f"P1: {p1_move} vs P2:{p2_move}"
                if p1_move == p2_move:
                    gameText += " | Draw!"
                elif p1_move == 'paper' and p2_move == 'rock':
                    gameText += " | P1 Wins!"
                elif p1_move == 'rock' and p2_move == 'scissors':
                    gameText += " | P1 Wins!"   
                elif p1_move == 'scissors' and p2_move == 'paper':
                    gameText += " | P1 Wins!"
                else:
                    gameText  += " | P2 Wins!"
            
            else:
                gameText = "Didnt play properly!"

        cv2.putText(frame, f"Clock: {clock}", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"GameText: {gameText}", (50, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2, cv2.LINE_AA)

        clock = (clock + 1) % 100
        
        cv2.imshow('Rock Paper Scissor', frame)

        if cv2.waitKey(1) == ord('q'):
            break

vid.release()
cv2.destroyAllWindows()
