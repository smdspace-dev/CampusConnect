# 🚀 Campus Connect - Render Deployment Guide

## 📋 Complete Step-by-Step Instructions

### 🎯 Prerequisites
- ✅ GitHub repository (you already have this with 519 commits!)
- ✅ Render account (free): https://render.com
- ✅ Your project pushed to GitHub

### 🔧 **Step 1: Prepare Your Render Account**

1. **Create Render Account:**
   - Go to https://render.com
   - Sign up with your GitHub account
   - Connect your GitHub repositories

2. **Connect GitHub Repository:**
   - In Render dashboard, click "New +"
   - Select "Connect Repository"
   - Find and connect your `CampusConnect` repository

### 🗄️ **Step 2: Create PostgreSQL Database**

1. **Create Database Service:**
   - In Render dashboard, click "New +"
   - Select "PostgreSQL"
   - Configuration:
     ```
     Name: campus-connect-db
     Database: campus_connect
     User: campus_connect_user
     Plan: Free
     ```

2. **Save Database Details:**
   - After creation, note the "Internal Database URL"
   - Format: `postgresql://username:password@hostname:port/database`
   - Keep this for backend configuration

### 🐍 **Step 3: Deploy Django Backend**

1. **Create Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Configuration:
     ```
     Name: campus-connect-backend
     Root Directory: backend
     Environment: Python 3
     Build Command: pip install -r requirements.txt
     Start Command: python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
     ```

2. **Environment Variables:**
   Add these in the "Environment" section:
   ```
   SECRET_KEY=your-auto-generated-secret-key
   DEBUG=False
   DATABASE_URL=postgresql://[from your database]
   ALLOWED_HOSTS=campus-connect-backend.onrender.com
   CORS_ALLOWED_ORIGINS=https://campus-connect-frontend.onrender.com
   ```

3. **Advanced Settings:**
   - Plan: Free
   - Auto-Deploy: Yes
   - Health Check Path: `/api/health/`

### ⚛️ **Step 4: Deploy React Frontend**

1. **Create Static Site:**
   - Click "New +" → "Static Site"
   - Connect your GitHub repo
   - Configuration:
     ```
     Name: campus-connect-frontend
     Root Directory: frontend
     Build Command: npm ci && npm run build
     Publish Directory: build
     ```

2. **Environment Variables:**
   ```
   REACT_APP_API_URL=https://campus-connect-backend.onrender.com/api
   ```

3. **Advanced Settings:**
   - Plan: Free
   - Auto-Deploy: Yes
   - Add redirect rule for SPA:
     ```
     /*    /index.html   200
     ```

### 🔧 **Step 5: Configure Your Local Files**

**Update your render.yaml (already done):**
The render.yaml file in your project root is configured for automatic deployment.

**Your project structure should look like:**
```
CampusConnect/
├── render.yaml                    ✅ (configured)
├── backend/
│   ├── requirements.txt          ✅ (updated with production deps)
│   ├── backend/
│   │   ├── settings.py          ✅ (production ready)
│   │   ├── health.py            ✅ (health check endpoint)
│   │   └── urls.py              ✅ (health endpoint added)
│   └── manage.py
├── frontend/
│   ├── package.json             ✅
│   ├── .env.example             ✅
│   └── src/
└── README.md                    ✅
```

### 🚀 **Step 6: Deploy Using render.yaml (Automated)**

**Option A: Automatic Deployment (Recommended)**
1. Your render.yaml file will automatically configure everything
2. Just push your code to GitHub
3. Render will detect the render.yaml and create all services

**Option B: Manual Setup**
Follow steps 2-4 above for manual configuration

### 🔍 **Step 7: Monitor Deployment**

1. **Check Build Logs:**
   - Go to each service in Render dashboard
   - Monitor "Events" tab for build progress
   - Check "Logs" for any errors

2. **Verify Services:**
   - Backend health check: `https://your-backend.onrender.com/api/health/`
   - Frontend: `https://your-frontend.onrender.com`
   - API docs: `https://your-backend.onrender.com/swagger/`

### 🏥 **Step 8: Database Setup**

1. **Run Migrations:**
   After backend deploys successfully:
   - Go to backend service dashboard
   - Use "Shell" tab to run:
     ```bash
     python manage.py migrate
     python manage.py createsuperuser
     ```

2. **Create Admin User:**
   ```bash
   python manage.py createsuperuser
   # Follow prompts to create admin account
   ```

### 🎯 **Step 9: Final Configuration**

1. **Update Frontend API URL:**
   - In Render frontend service
   - Add environment variable:
     ```
     REACT_APP_API_URL=https://[your-backend-url]/api
     ```

2. **Update Backend CORS:**
   - In backend environment variables:
     ```
     CORS_ALLOWED_ORIGINS=https://[your-frontend-url]
     ```

### 🔧 **Troubleshooting Common Issues**

**❌ Build Failures:**
- Check requirements.txt for missing dependencies
- Verify Python version compatibility
- Check logs in Render dashboard

**❌ Database Connection:**
- Verify DATABASE_URL format
- Check if database service is running
- Run migrations after first deployment

**❌ CORS Errors:**
- Update CORS_ALLOWED_ORIGINS with your frontend URL
- Check ALLOWED_HOSTS includes your backend domain

**❌ Static Files Not Loading:**
- Verify collectstatic runs during build
- Check WhiteNoise middleware is configured

### 📱 **Expected URLs After Deployment:**

```
Frontend: https://campus-connect-frontend.onrender.com
Backend:  https://campus-connect-backend.onrender.com
API:      https://campus-connect-backend.onrender.com/api/
Admin:    https://campus-connect-backend.onrender.com/admin/
Health:   https://campus-connect-backend.onrender.com/api/health/
Docs:     https://campus-connect-backend.onrender.com/swagger/
```

### 🔄 **Automatic Deployments:**

Every time you push to your main branch:
1. Render detects changes
2. Rebuilds affected services
3. Deploys automatically
4. Your 519 commits will show professional development history!

### 💡 **Pro Tips:**

1. **Free Tier Limitations:**
   - Services sleep after 15 minutes of inactivity
   - Database has storage limits
   - Consider upgrading for production use

2. **Performance:**
   - First request after sleep may be slow (cold start)
   - Consider paid plans for always-on services

3. **Monitoring:**
   - Use Render's built-in monitoring
   - Set up uptime monitoring for critical services

---

## 🎉 **You're Ready to Deploy!**

Your Campus Connect application is now fully configured for Render deployment. With your professional 519-commit history, this will look impressive on your portfolio!

**Need help?** Check the logs in your Render dashboard or refer to Render's documentation.