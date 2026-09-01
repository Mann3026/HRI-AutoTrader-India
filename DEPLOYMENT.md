# HRI AutoTrader - Deployment Guide

## Quick Deploy to Render (Free)

### Step 1: Push Code to GitHub
1. Go to https://github.com/new
2. Create a new repository (name: `HRI-AutoTrader-India`)
3. Follow GitHub instructions to push your local code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: AutoTrader with admin login, reporting, and signal config"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/HRI-AutoTrader-India.git
   git push -u origin main
   ```

### Step 2: Deploy on Render
1. Go to https://render.com (sign up free with GitHub)
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Fill in:
   - **Name:** `hri-autotrader`
   - **Runtime:** Python
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `python -m uvicorn backend.app:app --host 0.0.0.0 --port $PORT`
5. Click "Create Web Service"
6. Wait ~3 minutes for deployment
7. Get your live URL (like: `https://hri-autotrader-xxxxx.onrender.com`)

### Step 3: Update Frontend API URL
1. After deployment, update frontend to use live URL:
   - Open `frontend/app.js`
   - Replace `http://127.0.0.1:8000` with your Render URL
   - Example: `https://hri-autotrader-xxxxx.onrender.com`

### Step 4: Share with Others
- Share the live URL with testers
- Share your GitHub repo link for feedback
- Frontend works from the live backend

### Default Credentials
- Admin: `admin` / `admin123`
- Create users from the Controls section

### Notes
- Free tier sleeps after 15 mins of inactivity (wakes up on first request)
- Perfect for testing and feedback gathering
- Upgrade to paid if going to production

## Alternative: Deploy Frontend to Vercel (Free)
1. Push code to GitHub
2. Go to https://vercel.com
3. Import your repository
4. Deploy (automatic)
5. Update backend URL in frontend

This way backend runs on Render and frontend on Vercel!
