# Static Frontend Deployment Guide

## Files Needed for Frontend

Your static frontend consists of:
```
index.html
api.js
imgs/
  ├── asl_preview.jpg
  └── asl_images/
      └── (all ASL letter images)
```

## Deploy to Cloudflare Pages

### Method 1: Direct Upload

1. Go to [Cloudflare Pages](https://pages.cloudflare.com/)
2. Click "Create a project"
3. Choose "Direct Upload"
4. Upload these files:
   - `index.html`
   - `api.js`
   - `imgs/` folder (with all contents)
5. Deploy!

### Method 2: Git Integration

1. Create a new repository on GitHub
2. Push only frontend files:
   ```bash
   git init
   git add index.html api.js imgs/
   git commit -m "Initial frontend"
   git push
   ```
3. Connect repository to Cloudflare Pages
4. Build settings:
   - Build command: (leave empty)
   - Build output directory: `/`

## Deploy to Netlify

1. Go to [Netlify](https://www.netlify.com/)
2. Drag and drop your folder containing:
   - `index.html`
   - `api.js`
   - `imgs/`
3. Done!

## Deploy to GitHub Pages

1. Create repository named `username.github.io`
2. Push frontend files
3. Enable GitHub Pages in repository settings
4. Access at `https://username.github.io`

## Deploy to Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in your frontend folder
3. Follow prompts

## Local Testing

Simply open `index.html` in a browser, or use a local server:

```bash
# Python
python -m http.server 8000

# Node.js
npx serve

# PHP
php -S localhost:8000
```

Then visit `http://localhost:8000`

## Configuration

After deployment:
1. Open your deployed frontend URL
2. Enter your Colab backend URL (from Cloudflare tunnel)
3. Click "SET"
4. Video feed should start if backend is running

## Troubleshooting

### CORS Errors
- Ensure `flask-cors` is installed on backend
- Check that backend URL is correct (no trailing slash)

### Video Feed Not Loading
- Verify backend is running
- Check browser console for errors
- Ensure camera permissions are granted on backend server

### Backend Offline
- Colab session may have timed out
- Restart Cloudflare tunnel
- Check backend logs

## File Structure

```
frontend/
├── index.html          # Main page
├── api.js             # API communication
└── imgs/              # Static assets
    ├── asl_preview.jpg
    └── asl_images/
        └── *.jpg
```

## Notes

- Frontend is 100% static - no build process needed
- Backend URL is stored in browser localStorage
- Works on any static hosting platform
- No server-side rendering required
