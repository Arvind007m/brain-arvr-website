# GitHub & Render Deployment Guide

Follow these steps to deploy your Brain AR/VR website:

## Step 1: Initialize Git Repository

```bash
# Navigate to your project directory
cd brain_arvr_website

# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: Brain AR/VR Detection App"
```

## Step 2: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon → "New repository"
3. Repository name: `brain-arvr-website` (or your preferred name)
4. Make it Public (required for free Render hosting)
5. Don't initialize with README (we already have one)
6. Click "Create repository"

## Step 3: Connect Local Repository to GitHub

```bash
# Add GitHub as remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/brain-arvr-website.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Deploy to Render

1. Go to [Render.com](https://render.com) and sign up/sign in
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `brain-arvr-app`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python start.py`
5. Click "Create Web Service"

## Step 5: Upload Model File

⚠️ **Important**: The AI model file is too large for GitHub. You have two options:

### Option A: Direct Upload (Temporary)
1. After deployment, use Render's shell to upload the model:
   - Go to your service dashboard
   - Click "Shell" tab
   - Upload `3d_unet_brats2020.pth` to `backend/model/` directory

### Option B: Cloud Storage (Recommended)
1. Upload model to Google Drive, Dropbox, or AWS S3
2. Add download script to fetch model on startup
3. Modify `start.py` to download model if not present

## Step 6: Test Your Deployment

1. Wait for build to complete (~5-10 minutes)
2. Open your app URL (provided by Render)
3. Test file upload and 3D viewing functionality

## Troubleshooting

- **Build fails**: Check requirements.txt and Python version
- **Model missing**: Upload model file to backend/model/ directory
- **Frontend not loading**: Verify paths in main.py are correct
- **CORS errors**: Check CORS settings in main.py

## Production Notes

- Free tier has limitations (512MB RAM, sleeps after 15min inactivity)
- Consider upgrading to paid plan for production use
- Monitor logs through Render dashboard
- Set up custom domain in Render settings if needed 