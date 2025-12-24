# 🚀 DEPLOY NOW - Quick Reference

## ✅ Status: READY TO DEPLOY!

All code is pushed to GitHub: `https://github.com/Vicihka/madam-da-show-demo`

---

## 📋 Quick Steps

### 1. Go to Railway
🔗 [railway.app](https://railway.app) → Login with GitHub

### 2. Create Project
- **New Project** → **Deploy from GitHub repo**
- Select: `Vicihka/madam-da-show-demo`

### 3. Add PostgreSQL
- **+ New** → **Database** → **PostgreSQL**

### 4. Add Redis (Optional)
- **+ New** → **Database** → **Redis**

### 5. Set Environment Variables
Click your web service → **Variables** tab → Add these:

```env
SECRET_KEY=w0u!)5s5bjdae_5hqg=i14$7i(i)&(-owq)rdedi7q1f+_!90=
DEBUG=False
ALLOWED_HOSTS=*.railway.app
CSRF_TRUSTED_ORIGINS=https://*.railway.app
ENABLE_SSL_REDIRECT=True
BAKONG_ID=vicheka_yeun@wing
BAKONG_MERCHANT_NAME=MADAM DA
BAKONG_API_BASE=https://bakongapi.com
```

### 6. Generate Domain
- **Settings** → **Networking** → **Generate Domain**
- Get your URL: `https://your-app.up.railway.app`

### 7. Update Variables with Your Domain
Replace `*.railway.app` with your actual domain:
```env
ALLOWED_HOSTS=your-actual-domain.up.railway.app,*.railway.app
CSRF_TRUSTED_ORIGINS=https://your-actual-domain.up.railway.app
```

### 8. Run Migrations (Railway CLI)

Install CLI:
```bash
npm install -g @railway/cli
```

Login and link:
```bash
railway login
railway link
```

Run migrations:
```bash
railway run python manage.py migrate
railway run python manage.py collectstatic --noinput
railway run python manage.py createsuperuser
```

### 9. Test Your App
Visit: `https://your-app.up.railway.app`

---

## ⚡ That's It!

Your app is now live on Railway!

**For detailed steps, see:** `RAILWAY_DEPLOYMENT_STEPS.md`

---

## 🐛 If Something Goes Wrong

**Check logs:**
- Railway Dashboard → Deployments → View Logs

**Common fixes:**
- Missing environment variable? Add it in Variables tab
- Static files not loading? Run `railway run python manage.py collectstatic --noinput`
- Database error? PostgreSQL should auto-configure `DATABASE_URL`

---

## 📞 Quick Links

- 🚂 Railway: [railway.app/dashboard](https://railway.app/dashboard)
- 📖 Full Guide: `RAILWAY_DEPLOYMENT_STEPS.md`
- 🔧 Troubleshooting: `RAILWAY_DEPLOYMENT_GUIDE.md`
- 💳 Bakong Config: `BAKONG_CONFIGURATION.md`
- 🖼️ Image Setup: `IMAGE_SETUP_GUIDE.md`

---

**🎉 You're ready to deploy! Go to railway.app now!**

