# Deployment Guide

This app can be deployed to several free platforms. Here are the best options:

## Option 1: Render (Recommended - Easiest)

Render has a free tier that works great for Flask apps.

1. Sign up at https://render.com (free)
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Settings:
   - Name: reddit-calendar-generator
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Click "Create Web Service"

The app will be live at `https://your-app-name.onrender.com`

Note: Free tier spins down after 15 minutes of inactivity, so first request might be slow.

## Option 2: Railway

Railway gives you $5 free credit per month.

1. Sign up at https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select your repo
4. Railway auto-detects Flask, but you can set:
   - Start Command: `gunicorn app:app`
5. Deploy

Live at `https://your-app-name.up.railway.app`

## Option 3: Fly.io

Fly.io has a free tier.

1. Install flyctl: https://fly.io/docs/getting-started/installing-flyctl/
2. Sign up: `fly auth signup`
3. In your project folder: `fly launch`
4. Follow prompts
5. Deploy: `fly deploy`

## Option 4: PythonAnywhere

PythonAnywhere is specifically for Python apps, free tier available.

1. Sign up at https://www.pythonanywhere.com
2. Go to "Web" tab
3. Click "Add a new web app"
4. Choose Flask, Python 3.10
5. Upload your files or clone from GitHub
6. Set working directory and source code path
7. Reload web app

## Option 5: Replit

Replit can host Flask apps.

1. Sign up at https://replit.com
2. Import from GitHub
3. Run the app
4. Click "Deploy" button in sidebar
5. Follow prompts

## Important Notes

All platforms need:
- `gunicorn` in requirements.txt (already added)
- `Procfile` or start command set to `gunicorn app:app`
- Environment variables if needed (none required for this app)

The app uses local file storage (data/ folder), so on free tiers:
- Files persist between deployments on most platforms
- But if the instance restarts, you might lose data
- For production, consider using a database or cloud storage

## Quick Deploy to Render

Fastest way:

1. Push your code to GitHub
2. Go to https://render.com
3. New Web Service → Connect GitHub
4. Select repo
5. Use these settings:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
6. Deploy

Done! Your app will be live in a few minutes.

