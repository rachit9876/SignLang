# ASL Recognition - Static Frontend + API Backend

Real-time American Sign Language recognition system with separated frontend and backend.

## Architecture

```
┌─────────────────────┐         ┌──────────────────────┐
│  Static Frontend    │         │   Python Backend     │
│  (Cloudflare Pages) │ ◄─────► │  (Google Colab)      │
│                     │  HTTPS  │                      │
│  - index.html       │         │  - Flask API         │
│  - api.js           │         │  - MediaPipe         │
│  - imgs/            │         │  - ML Model          │
└─────────────────────┘         └──────────────────────┘
```

## Project Structure

```
SignLang/
├── Frontend (Static)
│   ├── index.html              # Main UI
│   ├── api.js                  # API communication
│   └── imgs/                   # Static assets
│
├── Backend (Python)
│   ├── app.py                  # Flask API server
│   ├── model.p                 # Trained ML model
│   ├── requirements.txt        # Python dependencies
│   └── templates/              # (Optional for local testing)
│
└── Documentation
    ├── README.md               # This file
    ├── COLAB_SETUP.md         # Backend deployment guide
    └── FRONTEND_DEPLOY.md     # Frontend deployment guide
```

## Quick Start

### 1. Deploy Backend (Google Colab)

See [COLAB_SETUP.md](COLAB_SETUP.md) for detailed instructions.

```python
# In Colab notebook
!pip install flask flask-cors opencv-python mediapipe scikit-learn numpy
!cloudflared tunnel --url http://localhost:5000
# Copy the generated URL
```

### 2. Deploy Frontend (Cloudflare Pages)

See [FRONTEND_DEPLOY.md](FRONTEND_DEPLOY.md) for detailed instructions.

1. Upload `index.html`, `api.js`, and `imgs/` folder
2. Deploy to any static hosting (Cloudflare Pages, Netlify, GitHub Pages)
3. Open deployed site
4. Enter your Colab backend URL
5. Start using!

## Features

- ✅ Real-time ASL recognition
- ✅ Multiple camera support
- ✅ Text accumulation (hold sign for 3 seconds)
- ✅ Backspace and clear functions
- ✅ ASL reference guide
- ✅ Backend status indicator
- ✅ Automatic reconnection
- ✅ Error handling
- ✅ Mobile responsive

## API Endpoints

### Backend API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Check backend status |
| `/video_feed?camera=0` | GET | Video stream with predictions |
| `/get_text` | GET | Get accumulated text |
| `/clear_text` | POST | Clear accumulated text |
| `/backspace` | POST | Remove last character |

## Technology Stack

### Frontend
- Pure HTML/CSS/JavaScript
- No frameworks or build tools
- Fetch API for HTTP requests
- LocalStorage for configuration

### Backend
- Python 3.8+
- Flask (Web framework)
- Flask-CORS (Cross-origin support)
- OpenCV (Video processing)
- MediaPipe (Hand detection)
- scikit-learn (ML model)

## Development

### Local Backend Testing

```bash
pip install -r requirements.txt
python app.py
# Backend runs on http://localhost:5000
```

### Local Frontend Testing

```bash
# Open index.html in browser, or:
python -m http.server 8000
# Visit http://localhost:8000
```

## Configuration

### Change Backend URL

1. Open frontend in browser
2. Enter new URL in backend configuration field
3. Click "SET"
4. URL is saved in browser localStorage

### Change Camera

Use the camera dropdown to switch between available cameras (0-3).

## Troubleshooting

### Backend Offline
- Check if Colab session is active
- Restart Cloudflare tunnel
- Verify backend URL is correct

### Video Feed Not Loading
- Ensure backend has camera access
- Check CORS is enabled
- Verify network connectivity

### CORS Errors
- Ensure `flask-cors` is installed
- Check backend logs for errors

## License

See [LICENSE](LICENSE) file.

## Credits

- MediaPipe by Google
- ASL dataset and model training
- Flask web framework

## Support

For issues and questions:
1. Check documentation files
2. Review browser console for errors
3. Check backend logs in Colab
