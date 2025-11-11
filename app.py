import pickle
import cv2
import mediapipe as mp
import numpy as np
from flask import Flask, render_template, Response, request, jsonify

app = Flask(__name__)

model = pickle.load(open('./model.p', 'rb'))['model']
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.5)

def generate_frames(camera_id=0):
    cap = cv2.VideoCapture(camera_id)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                data_aux = []
                x_ = [lm.x for lm in hand_landmarks.landmark]
                y_ = [lm.y for lm in hand_landmarks.landmark]
                
                for lm in hand_landmarks.landmark:
                    data_aux.append(lm.x - min(x_))
                    data_aux.append(lm.y - min(y_))
                
                prediction = model.predict([np.asarray(data_aux)])
                proba = model.predict_proba([np.asarray(data_aux)])[0]
                confidence = max(proba) * 100
                cv2.putText(frame, f"{prediction[0]} ({confidence:.0f}%)", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    camera_id = request.args.get('camera', default=0, type=int)
    return Response(generate_frames(camera_id), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def capture():
    camera_id = request.args.get('camera', default=0, type=int)
    cap = cv2.VideoCapture(camera_id)
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        return jsonify({'message': 'Failed to capture frame'})
    
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        data_aux = []
        x_ = [lm.x for lm in hand_landmarks.landmark]
        y_ = [lm.y for lm in hand_landmarks.landmark]
        
        for lm in hand_landmarks.landmark:
            data_aux.append(lm.x - min(x_))
            data_aux.append(lm.y - min(y_))
        
        prediction = model.predict([np.asarray(data_aux)])
        proba = model.predict_proba([np.asarray(data_aux)])[0]
        
        classes = model.classes_
        results_text = f"Predicted: {prediction[0]}<br><br>All probabilities:<br>"
        for cls, prob in sorted(zip(classes, proba), key=lambda x: x[1], reverse=True):
            results_text += f"{cls}: {prob*100:.1f}%<br>"
        
        return jsonify({'message': results_text})
    else:
        return jsonify({'message': 'No hand detected'})

if __name__ == '__main__':
    app.run(debug=True)
