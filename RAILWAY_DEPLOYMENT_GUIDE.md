# 🚂 Railway Deployment Guide for MADAM DA E-Commerce

## ✅ Is Railway Good for Your Demo?

**YES! Railway is an excellent choice for client demos because:**

1. ✅ **Free Tier Available** - Perfect for demos and testing
2. ✅ **Easy Setup** - Deploy in minutes, not hours
3. ✅ **Built-in PostgreSQL** - No separate database setup needed
4. ✅ **Automatic Deployments** - Push to Git, auto-deploy
5. ✅ **Environment Variables** - Easy secret management
6. ✅ **Custom Domains** - Get a `.railway.app` domain instantly
7. ✅ **HTTPS by Default** - SSL certificates included
8. ✅ **Good Performance** - Fast enough for demos and small projects

---

## 📋 Pre-Deployment Checklist

Before deploying, make sure:

- [ ] Your code is pushed to GitHub/GitLab/Bitbucket
- [ ] You have a Railway account (sign up at [railway.app](https://railway.app))
- [ ] You know your secret keys (SECRET_KEY, Telegram tokens, etc.)
- [ ] You've tested locally with `DEBUG=False`

---

## 🚀 Step-by-Step Deployment

### Step 1: Create Railway Account & Project

1. Go to [railway.app](https://railway.app) and sign up (GitHub login recommended)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"** (or GitLab/Bitbucket)
4. Select your repository
5. Railway will auto-detect Django and start building

### Step 2: Add PostgreSQL Database

1. In your Railway project dashboard, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway will automatically create a PostgreSQL database
4. The `DATABASE_URL` environment variable will be automatically set

### Step 3: Add Redis (Optional but Recommended)

**For WebSocket and caching support:**

1. Click **"+ New"** → **"Database"** → **"Add Redis"**
2. Railway will create a Redis instance
3. The `REDIS_URL` environment variable will be automatically set

**Note:** If you don't add Redis, WebSocket features won't work, but the rest of the app will function.

### Step 4: Configure Environment Variables

In Railway dashboard, go to your service → **"Variables"** tab, and add:

#### Required Variables:

```env
# Django Settings
SECRET_KEY=your-super-secret-key-here-generate-a-new-one
DEBUG=False
ALLOWED_HOSTS=*.railway.app,your-custom-domain.com

# CSRF Trusted Origins (add your Railway domain)
CSRF_TRUSTED_ORIGINS=https://*.railway.app,https://your-custom-domain.com

# SSL Redirect (Railway handles HTTPS automatically)
ENABLE_SSL_REDIRECT=True
```

#### Optional Variables (if you use these features):

```env
# Telegram Bot (if you use it)
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-telegram-chat-id

# Bakong Payment (if you use it)
BAKONG_ID=your-bakong-id
BAKONG_MERCHANT_NAME=MADAM DA
BAKONG_API_BASE=https://bakongapi.com

# CORS (if you have a frontend)
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

**Important Notes:**
- `DATABASE_URL` and `REDIS_URL` are automatically set by Railway - **don't override them**
- Generate a new `SECRET_KEY` for production (use: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- Replace `*.railway.app` with your actual Railway domain after deployment

### Step 5: Update Procfile (if needed)

Your current `Procfile` uses Gunicorn (WSGI), which is good for HTTP requests. However, if you need **WebSocket support**, you have two options:

#### Option A: Keep Gunicorn (Recommended for demos)
- ✅ Simpler setup
- ✅ Works for most features
- ❌ WebSocket won't work

Your current `Procfile` is fine:
```
web: gunicorn project.wsgi:application --bind 0.0.0.0:$PORT
```

#### Option B: Use Daphne (For full WebSocket support)
- ✅ Full WebSocket support
- ⚠️ Slightly more complex

Update `Procfile` to:
```
web: daphne -b 0.0.0.0 -p $PORT project.asgi:application
```

**For a client demo, Option A (Gunicorn) is usually sufficient unless WebSocket is critical.**

### Step 6: Update Settings for Railway

Your `settings.py` already supports Railway! Just make sure:

1. ✅ `dj-database-url` is in `requirements.txt` (it is!)
2. ✅ `DATABASE_URL` is used (your settings already do this)
3. ✅ `REDIS_URL` is used (your settings already do this)

### Step 7: Deploy!

1. Railway will automatically detect your `Procfile` and `requirements.txt`
2. It will build and deploy your app
3. Check the **"Deployments"** tab for build logs
4. Once deployed, Railway will give you a URL like: `https://your-app-name.up.railway.app`

### Step 8: Run Migrations

After first deployment:

1. Go to your service → **"Settings"** → **"Deploy"**
2. Add a **"Deploy Command"**:
   ```
   python manage.py migrate && python manage.py collectstatic --noinput
   ```
3. Or run manually via Railway CLI (see below)

### Step 9: Create Superuser

You need to create an admin user. Use Railway CLI:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Run Django shell
railway run python manage.py createsuperuser
```

Or use Railway's web console:
1. Go to your service → **"Settings"** → **"Deploy"**
2. Add a one-time command in "Deploy Command" (remove after first run)

---

## 🔧 Important Configuration Updates

### Update ALLOWED_HOSTS After Deployment

Once Railway gives you your domain, update the `ALLOWED_HOSTS` environment variable:

```env
ALLOWED_HOSTS=your-app-name.up.railway.app,*.railway.app
```

### Update CSRF_TRUSTED_ORIGINS

```env
CSRF_TRUSTED_ORIGINS=https://your-app-name.up.railway.app
```

---

## 📁 Static Files & Media

### Static Files
✅ **Already configured!** Your `settings.py` uses WhiteNoise, which works perfectly on Railway.

Make sure to run:
```bash
python manage.py collectstatic --noinput
```

Railway will automatically run this if you add it to your deploy command.

### Media Files (Uploads)

⚠️ **Important:** Railway's filesystem is **ephemeral** - uploaded files will be lost on redeploy!

**Solutions:**

1. **For Demo:** Accept that media files may be lost (usually fine for demos)
2. **For Production:** Use cloud storage:
   - AWS S3
   - Cloudinary
   - Railway Volume (persistent storage)

**Quick fix for demo:** Add to your deploy command:
```bash
mkdir -p media && python manage.py migrate && python manage.py collectstatic --noinput
```

---

## 🐛 Troubleshooting

### Build Fails

**Check:**
- ✅ `requirements.txt` is correct
- ✅ `runtime.txt` specifies Python version (you have `python-3.11.9`)
- ✅ All dependencies are listed

### App Crashes on Startup

**Check logs:**
1. Go to **"Deployments"** → Click on latest deployment → **"View Logs"**
2. Common issues:
   - Missing `SECRET_KEY` → Add to environment variables
   - Missing `ALLOWED_HOSTS` → Add to environment variables
   - Database connection error → Check `DATABASE_URL` is set

### Static Files Not Loading

**Fix:**
1. Make sure `collectstatic` runs: Add to deploy command
2. Check `STATIC_ROOT` is set correctly (it is: `staticfiles`)
3. Verify WhiteNoise is in `MIDDLEWARE` (it is!)

### WebSocket Not Working

**If using Gunicorn:**
- WebSocket requires Daphne (ASGI), not Gunicorn (WSGI)
- Switch `Procfile` to use Daphne (see Step 5, Option B)

**If using Daphne:**
- Make sure Redis is added and `REDIS_URL` is set
- Check `CHANNEL_LAYERS` configuration in `settings.py`

---

## 💰 Railway Pricing

### Free Tier (Hobby Plan)
- ✅ $5 free credit per month
- ✅ Perfect for demos and small projects
- ✅ Auto-sleeps after inactivity (wakes on request)
- ⚠️ Limited resources

### Paid Plans
- **Developer:** $5/month + usage
- **Team:** $20/month + usage
- **Enterprise:** Custom pricing

**For a client demo, the free tier is usually sufficient!**

---

## 🔐 Security Checklist

Before showing to client:

- [ ] `DEBUG=False` in environment variables
- [ ] `SECRET_KEY` is set and secure
- [ ] `ALLOWED_HOSTS` includes your Railway domain
- [ ] `CSRF_TRUSTED_ORIGINS` includes your Railway domain
- [ ] Admin URL is changed (if needed)
- [ ] Strong admin password set
- [ ] HTTPS is enabled (Railway does this automatically)

---

## 📊 Monitoring & Logs

### View Logs
1. Go to your service → **"Deployments"**
2. Click on a deployment → **"View Logs"**
3. Or use Railway CLI: `railway logs`

### Monitor Performance
- Railway dashboard shows CPU, Memory, Network usage
- Check logs for errors

---

## 🎯 Quick Start Commands

### Deploy Command (add in Railway Settings → Deploy)
```bash
python manage.py migrate && python manage.py collectstatic --noinput
```

### One-time Commands (via Railway CLI)
```bash
# Create superuser
railway run python manage.py createsuperuser

# Run migrations manually
railway run python manage.py migrate

# Collect static files
railway run python manage.py collectstatic --noinput

# Django shell
railway run python manage.py shell
```

---

## ✅ Post-Deployment Checklist

After deployment:

- [ ] App loads at Railway URL
- [ ] Admin panel accessible (`/admin/`)
- [ ] Static files loading (CSS, JS, images)
- [ ] Database working (can create/view data)
- [ ] Forms submitting correctly
- [ ] No errors in logs
- [ ] Test on mobile device (if needed)

---

## 🚀 Next Steps

1. **Custom Domain (Optional):**
   - Go to **"Settings"** → **"Domains"**
   - Add your custom domain
   - Update `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`

2. **Backup Database:**
   - Railway PostgreSQL can be backed up
   - Use `pg_dump` via Railway CLI

3. **Scale Up (if needed):**
   - Upgrade plan for more resources
   - Add more workers for better performance

---

## 📞 Support

- **Railway Docs:** [docs.railway.app](https://docs.railway.app)
- **Railway Discord:** [discord.gg/railway](https://discord.gg/railway)
- **Your Project Docs:** Check `README.md` and other guides in your project

---

## 🎉 You're Ready!

Railway is perfect for your client demo. It's:
- ✅ Fast to set up
- ✅ Free tier available
- ✅ Professional looking
- ✅ Easy to maintain

Good luck with your demo! 🚀

