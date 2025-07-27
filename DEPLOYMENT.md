# Vercel Deployment Guide

## Option 1: Full-Stack Vercel Deployment (Recommended)

This deploys both your Flask backend and frontend together on Vercel.

### Prerequisites
1. Install Vercel CLI: `npm install -g vercel`
2. Create a Vercel account at https://vercel.com

### Deployment Steps

1. **Install Flask-CORS locally (for testing)**:
   ```bash
   pip install Flask-CORS==4.0.0
   ```

2. **Test locally** (optional):
   ```bash
   python app.py
   ```

3. **Deploy to Vercel**:
   ```bash
   vercel --prod
   ```

4. **Configure Environment Variables** (in Vercel dashboard):
   - Go to your project settings in Vercel
   - Add environment variables:
     - `FLASK_ENV` = `production`
     - `DEBUG` = `False`

### Important Notes:
- ✅ No localhost URLs to change - all API calls use relative paths
- ✅ Database persists between requests (JSON file storage)
- ✅ Real-time features work with auto-refresh
- ✅ Static files (CSS/JS) served correctly

---

## Option 2: Separate Frontend/Backend Deployment

If you prefer to deploy them separately:

### Backend (Flask API):
- Deploy on: Railway, Render, or Heroku
- Update frontend API URLs to point to your backend URL

### Frontend (Static):
- Deploy on: Vercel, Netlify, or GitHub Pages
- Update `app.js` to use your backend API URL

### Required Changes for Option 2:
1. Replace relative API calls in `app.js` with full URLs:
   ```javascript
   // Change from:
   fetch('/api/deals')
   
   // Change to:
   const API_BASE = 'https://your-backend.railway.app';
   fetch(`${API_BASE}/api/deals`)
   ```

---

## Recommended: Option 1 (Full-Stack)

Option 1 is simpler because:
- No URL changes needed
- Single deployment
- Vercel handles routing automatically
- No CORS issues
- Easier maintenance

## Testing Your Deployment

After deployment, test these features:
1. ✅ Create new deals with supplier names
2. ✅ Join deals with vendor names + locations  
3. ✅ Auto-refresh functionality
4. ✅ Real-time notifications
5. ✅ Database persistence

Your app is ready to deploy! 🚀
