# ⚡ Quick Start Guide

## 🎯 Goal
Deploy ASL Recognition app with:
- **Frontend**: Cloudflare Pages (static)
- **Backend**: Google Colab (Python API)

---

## 📦 What You Need

### Frontend Files
```
index.html
api.js
imgs/
  ├── asl_preview.jpg
  └── asl_images/ (28 images)
```

### Backend Files
```
app.py
model.p
requirements.txt
```

---

## 🚀 Deploy in 5 Minutes

### 1️⃣ Deploy Backend (2 min)

**Open Google Colab** → New Notebook → Run:

```python
# Upload app.py, model.p, requirements.txt first

# Install dependencies
!pip install flask flask-cors opencv-python mediapipe scikit-learn numpy

# Start Flask in background
from threading import Thread
import os

def run_flask():
    os.system('python app.py')

Thread(target=run_flask).start()

# Expose via Cloudflare Tunnel
!wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
!dpkg -i cloudflared-linux-amd64.deb
!cloudflared tunnel --url http://localhost:5000
```

**Copy the URL** that looks like: `https://xxxxx.trycloudflare.com`

---

### 2️⃣ Deploy Frontend (2 min)

**Option A: Cloudflare Pages**
1. Go to https://pages.cloudflare.com/
2. Click "Create a project" → "Direct Upload"
3. Upload: `index.html`, `api.js`, `imgs/` folder
4. Click "Deploy"
5. Copy your site URL

**Option B: Netlify**
1. Go to https://app.netlify.com/
2. Drag and drop folder with `index.html`, `api.js`, `imgs/`
3. Done!

---

### 3️⃣ Connect (1 min)

1. Open your deployed frontend URL
2. Paste backend URL in the configuration field
3. Click "SET"
4. ✅ Green indicator = Connected!

---

## 🧪 Test Locally First

### Start Backend
```bash
pip install -r requirements.txt
python app.py
```

### Test Backend
Open `test_local.html` in browser → Click "Test Connection"

### Open Frontend
Open `index.html` in browser → Enter `http://localhost:5000` → Click "SET"

---

## 📱 Usage

1. **Allow camera access** when prompted
2. **Hold an ASL sign** in front of camera
3. **Wait 3 seconds** for letter to be added
4. **Use BACK** to remove last character
5. **Use CLEAR** to reset text
6. **Click ? HELP** for ASL reference

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend Offline | Restart Colab, check tunnel |
| Video not loading | Verify backend URL, check CORS |
| CORS error | Ensure `flask-cors` installed |
| Colab timeout | Keep notebook active, use Colab Pro |

---

## 📚 Full Documentation

- **Complete Guide**: `README.md`
- **Backend Setup**: `COLAB_SETUP.md`
- **Frontend Deploy**: `FRONTEND_DEPLOY.md`
- **Migration Details**: `MIGRATION_SUMMARY.md`
- **Deployment Checklist**: `DEPLOYMENT_CHECKLIST.md`

---

## 🎉 That's It!

Your app is now live:
- ✅ Frontend on global CDN
- ✅ Backend processing ML predictions
- ✅ Real-time ASL recognition
- ✅ Mobile responsive

**Share your frontend URL and start recognizing signs!** 🤟

---

## 💡 Pro Tips

1. **Keep Colab Alive**: Run a cell every 30 minutes or use Colab Pro
2. **Save Backend URL**: Frontend saves it in localStorage
3. **Multiple Backends**: Switch between dev/prod by changing URL
4. **Custom Domain**: Add custom domain in Cloudflare Pages settings
5. **Analytics**: Add Google Analytics to `index.html` if needed

---

## 🆘 Need Help?

1. Check browser console (F12)
2. Check Colab logs
3. Review documentation files
4. Test with `test_local.html`
5. Verify all files uploaded correctly

---

## 🔗 Quick Links

- **Cloudflare Pages**: https://pages.cloudflare.com/
- **Google Colab**: https://colab.research.google.com/
- **Netlify**: https://www.netlify.com/
- **GitHub Pages**: https://pages.github.com/

---

**Happy Signing! 🤟✨**
