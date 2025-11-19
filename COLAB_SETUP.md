# Google Colab Backend Setup Guide

## Step 1: Upload Files to Colab

Upload these files to your Colab environment:
- `app.py`
- `model.p`
- `requirements.txt`
- `templates/index.html` (optional, for testing)
- `imgs/` folder (optional, for testing)

## Step 2: Install Dependencies

```python
!pip install -q flask flask-cors opencv-python mediapipe scikit-learn numpy
```

## Step 3: Start Flask Server

```python
from threading import Thread
import os

# Change to your project directory if needed
# os.chdir('/content/your-project-folder')

def run_flask():
    os.system('python app.py')

# Start Flask in background
thread = Thread(target=run_flask)
thread.start()
```

## Step 4: Setup Cloudflare Tunnel

```python
# Install cloudflared
!wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
!dpkg -i cloudflared-linux-amd64.deb

# Start tunnel (this will give you a public URL)
!cloudflared tunnel --url http://localhost:5000
```

## Step 5: Copy the Cloudflare URL

Look for output like:
```
Your quick Tunnel has been created! Visit it at:
https://xxxxx-xxxx-xxxx.trycloudflare.com
```

Copy this URL and paste it into your frontend's backend URL field.

## Alternative: Use ngrok

```python
# Install pyngrok
!pip install pyngrok

from pyngrok import ngrok

# Start ngrok tunnel
public_url = ngrok.connect(5000)
print(f"Backend URL: {public_url}")
```

## Testing the Backend

```python
import requests

# Test health endpoint
response = requests.get('http://localhost:5000/health')
print(response.json())
```

## Important Notes

1. **Camera Access**: Colab doesn't have direct camera access. The video feed will only work if you're running the backend locally or on a server with camera access.

2. **For Colab**: You may need to modify the app to accept base64 encoded images from the frontend instead of using direct camera access.

3. **Keep Alive**: Colab sessions timeout after inactivity. Keep the notebook active or use Colab Pro.

4. **CORS**: Already configured in app.py to allow cross-origin requests.

## Modified Backend for Image Upload (Optional)

If you want to send images from frontend camera instead of streaming:

```python
@app.route('/api/predict', methods=['POST'])
def predict_image():
    data = request.json
    image_data = data.get('image')  # base64 encoded image
    
    # Decode base64 image
    import base64
    img_bytes = base64.b64decode(image_data.split(',')[1])
    nparr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Process frame with mediapipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        # ... prediction logic ...
        return jsonify({'prediction': detected_letter, 'confidence': confidence})
    
    return jsonify({'prediction': None, 'confidence': 0})
```
