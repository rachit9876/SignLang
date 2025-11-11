import pickle
import cv2
import mediapipe as mp
import numpy as np
import time
from flask import Flask, render_template, Response, request, jsonify, send_from_directory

app = Flask(__name__)

model = pickle.load(open('./model.p', 'rb'))['model']
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.5)

current_letter = None
letter_start_time = None
accumulated_text = ""

def generate_frames(camera_id=0):
    global current_letter, letter_start_time, accumulated_text
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
                detected_letter = str(prediction[0])
                
                if detected_letter == current_letter:
                    elapsed = time.time() - letter_start_time
                    if elapsed >= 3.0 and current_letter:
                        accumulated_text += ' ' if current_letter.lower() == 'space' else current_letter
                        current_letter = None
                        letter_start_time = None
                    else:
                        cv2.putText(frame, f"{detected_letter} ({elapsed:.1f}s)", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3)
                else:
                    current_letter = detected_letter
                    letter_start_time = time.time()
                    cv2.putText(frame, f"{detected_letter} ({confidence:.0f}%)", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3)
        else:
            current_letter = None
            letter_start_time = None
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/imgs/<path:filename>')
def serve_image(filename):
    return send_from_directory('imgs', filename)

@app.route('/video_feed')
def video_feed():
    camera_id = request.args.get('camera', default=0, type=int)
    return Response(generate_frames(camera_id), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_text')
def get_text():
    return jsonify({'text': accumulated_text})

@app.route('/clear_text', methods=['POST'])
def clear_text():
    global accumulated_text
    accumulated_text = ""
    return jsonify({'status': 'ok'})

@app.route('/backspace', methods=['POST'])
def backspace():
    global accumulated_text
    accumulated_text = accumulated_text[:-1]
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
