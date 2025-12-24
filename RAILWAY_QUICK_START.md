# 🚂 Railway Quick Start - 5 Minute Deploy

## ✅ Yes, Railway is Perfect for Your Demo!

Railway is an **excellent choice** for client demos:
- ✅ Free tier available ($5 credit/month)
- ✅ Deploy in 5 minutes
- ✅ Automatic HTTPS
- ✅ Built-in PostgreSQL & Redis
- ✅ Professional `.railway.app` domain

---

## 🚀 5-Minute Deployment

### 1. Push to GitHub
```bash
git add .
git commit -m "Ready for Railway deployment"
git push
```

### 2. Create Railway Project
1. Go to [railway.app](https://railway.app) → Sign up
2. **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Railway auto-detects Django ✅

### 3. Add Database
1. Click **"+ New"** → **"Database"** → **"Add PostgreSQL"**
2. `DATABASE_URL` is auto-set ✅

### 4. Add Redis (Optional - for WebSocket)
1. Click **"+ New"** → **"Database"** → **"Add Redis"**
2. `REDIS_URL` is auto-set ✅

### 5. Set Environment Variables
Go to your service → **"Variables"** → Add:

```env
SECRET_KEY=generate-new-secret-key-here
DEBUG=False
ALLOWED_HOSTS=*.railway.app
CSRF_TRUSTED_ORIGINS=https://*.railway.app
ENABLE_SSL_REDIRECT=True
```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Add Deploy Command
Go to **"Settings"** → **"Deploy"** → **"Deploy Command"**:
```bash
python manage.py migrate && python manage.py collectstatic --noinput
```

### 7. Deploy!
Railway automatically deploys. Wait 2-3 minutes, then:
- Get your URL: `https://your-app.up.railway.app`
- Update `ALLOWED_HOSTS` with your actual domain
- Create superuser (see below)

---

## 👤 Create Admin User

### Option 1: Railway CLI (Recommended)
```bash
npm i -g @railway/cli
railway login
railway link
railway run python manage.py createsuperuser
```

### Option 2: One-time Deploy Command
Temporarily add to deploy command (remove after first run):
```bash
python manage.py migrate && python manage.py collectstatic --noinput && python manage.py createsuperuser --noinput --username admin --email admin@example.com
```
Then set password via Django shell.

---

## 🔧 Update After First Deploy

Once you get your Railway URL (e.g., `https://madamda-production.up.railway.app`):

1. Update `ALLOWED_HOSTS`:
   ```env
   ALLOWED_HOSTS=madamda-production.up.railway.app,*.railway.app
   ```

2. Update `CSRF_TRUSTED_ORIGINS`:
   ```env
   CSRF_TRUSTED_ORIGINS=https://madamda-production.up.railway.app
   ```

3. Redeploy (Railway auto-redeploys when env vars change)

---

## ✅ Your Project is Already Railway-Ready!

Your project already has:
- ✅ `Procfile` configured
- ✅ `requirements.txt` with all dependencies
- ✅ `runtime.txt` with Python version
- ✅ Environment variable support in `settings.py`
- ✅ WhiteNoise for static files
- ✅ PostgreSQL support via `dj-database-url`

**No code changes needed!** Just deploy! 🎉

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Build fails | Check `requirements.txt` and `runtime.txt` |
| App crashes | Check logs → Usually missing `SECRET_KEY` or `ALLOWED_HOSTS` |
| Static files 404 | Add `collectstatic` to deploy command |
| Database error | Check `DATABASE_URL` is set (auto-set by Railway) |
| WebSocket not working | Switch `Procfile` to use Daphne (see full guide) |

---

## 📋 Environment Variables Checklist

**Required:**
- [ ] `SECRET_KEY` (generate new one!)
- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS=*.railway.app` (update with your domain after deploy)

**Auto-set by Railway (don't override):**
- ✅ `DATABASE_URL` (from PostgreSQL service)
- ✅ `REDIS_URL` (from Redis service, if added)
- ✅ `PORT` (Railway sets this)

**Optional:**
- `TELEGRAM_BOT_TOKEN` (if using Telegram)
- `TELEGRAM_CHAT_ID` (if using Telegram)
- `BAKONG_ID` (if using Bakong payments)

---

## 🎯 What Happens Next?

1. **Railway builds your app** (2-3 minutes)
2. **App starts automatically**
3. **You get a URL** like `https://your-app.up.railway.app`
4. **Run migrations** (via deploy command)
5. **Create superuser** (via Railway CLI)
6. **Test your app!** 🎉

---

## 💡 Pro Tips

1. **Free tier auto-sleeps** - First request may be slow (wakes up)
2. **Media files are ephemeral** - They'll be lost on redeploy (fine for demos)
3. **Check logs** - Railway dashboard → Deployments → View Logs
4. **Custom domain** - Add in Settings → Domains (free on Railway)

---

## 📚 Full Guide

See `RAILWAY_DEPLOYMENT_GUIDE.md` for detailed instructions.

---

**Ready to deploy? Go to [railway.app](https://railway.app) and get started!** 🚀

