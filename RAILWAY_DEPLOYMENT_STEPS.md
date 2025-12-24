# 🚂 Railway Deployment - Step by Step (Zero Errors)

## ✅ Pre-Deployment Checklist

- [x] Code pushed to GitHub ✅
- [x] `Procfile` configured ✅
- [x] `requirements.txt` complete ✅
- [x] `runtime.txt` set (Python 3.11.9) ✅
- [x] Environment variable support ✅
- [x] Static files configuration ✅
- [x] All bugs fixed ✅

---

## 🚀 Step 1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"** or **"Login with GitHub"**
3. Authorize Railway to access your GitHub account

---

## 🚀 Step 2: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose repository: **`Vicihka/madam-da-show-demo`**
4. Click **"Deploy Now"**

Railway will start building automatically!

---

## 🚀 Step 3: Add PostgreSQL Database

1. In your Railway project dashboard
2. Click **"+ New"** button
3. Select **"Database"**
4. Choose **"Add PostgreSQL"**
5. Railway automatically creates the database
6. `DATABASE_URL` environment variable is automatically set ✅

---

## 🚀 Step 4: Add Redis (Optional - For WebSocket)

1. Click **"+ New"** again
2. Select **"Database"**
3. Choose **"Add Redis"**
4. `REDIS_URL` is automatically set ✅

**Note:** If you skip Redis, WebSocket won't work but everything else will.

---

## 🚀 Step 5: Configure Environment Variables

Click on your **web service** → Go to **"Variables"** tab

### Add These Variables:

```env
# Django Core (REQUIRED)
SECRET_KEY=<YOUR_SECRET_KEY_FROM_BELOW>
DEBUG=False

# Allowed Hosts (REQUIRED)
ALLOWED_HOSTS=*.railway.app

# CSRF Trusted Origins (REQUIRED)
CSRF_TRUSTED_ORIGINS=https://*.railway.app

# SSL (REQUIRED)
ENABLE_SSL_REDIRECT=True

# Bakong Payment (REQUIRED)
BAKONG_ID=vicheka_yeun@wing
BAKONG_MERCHANT_NAME=MADAM DA
BAKONG_API_BASE=https://bakongapi.com
```

### Optional Variables:

```env
# Telegram (Optional - for order notifications)
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id

# Admin URL (Optional - for security)
ADMIN_URL=secure-admin/
```

---

## 🔑 Your Generated SECRET_KEY

**Copy this SECRET_KEY and use it in Railway:**

```
w0u!)5s5bjdae_5hqg=i14$7i(i)&(-owq)rdedi7q1f+_!90=
```

⚠️ **IMPORTANT:** Keep this secret! Never share it publicly.

---

## 🚀 Step 6: Configure Build & Deploy

1. Go to **"Settings"** tab
2. Scroll to **"Deploy"** section
3. Add **"Build Command"** (leave empty or default)
4. Add **"Start Command"** (should auto-detect from Procfile):
   ```
   gunicorn project.wsgi:application --bind 0.0.0.0:$PORT
   ```

---

## 🚀 Step 7: Run Database Migrations

After first deployment, you need to run migrations:

### Option A: Railway CLI (Recommended)

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Link to your project:**
   ```bash
   railway link
   ```

4. **Run migrations:**
   ```bash
   railway run python manage.py migrate
   railway run python manage.py collectstatic --noinput
   ```

5. **Create superuser:**
   ```bash
   railway run python manage.py createsuperuser
   ```

### Option B: One-Time Deploy Command

1. Go to **"Settings"** → **"Deploy"**
2. Temporarily set **"Build Command"**:
   ```
   python manage.py migrate && python manage.py collectstatic --noinput
   ```
3. Click **"Deploy"**
4. After successful deployment, **remove the build command**

---

## 🚀 Step 8: Get Your Railway URL

1. Go to **"Settings"** → **"Networking"**
2. Click **"Generate Domain"**
3. You'll get a URL like: `https://madam-da-show-demo-production.up.railway.app`

---

## 🚀 Step 9: Update Environment Variables with Your Domain

Now that you have your Railway URL, update these variables:

1. Go to **"Variables"** tab
2. Update:
   ```env
   ALLOWED_HOSTS=madam-da-show-demo-production.up.railway.app,*.railway.app
   CSRF_TRUSTED_ORIGINS=https://madam-da-show-demo-production.up.railway.app
   ```
3. Click **"Deploy"** to apply changes

---

## 🚀 Step 10: Create Admin User

### Using Railway CLI:
```bash
railway run python manage.py createsuperuser
```

Follow the prompts:
- Username: `admin` (or your choice)
- Email: your email
- Password: strong password

---

## 🚀 Step 11: Test Your Deployment

1. **Visit your Railway URL:**
   ```
   https://your-app.up.railway.app
   ```

2. **Test these pages:**
   - [ ] Homepage loads ✅
   - [ ] Products display with images ✅
   - [ ] Add to cart works ✅
   - [ ] Checkout page loads ✅
   - [ ] KHQR payment generates QR code ✅
   - [ ] Admin panel accessible (`/admin/`) ✅

3. **Check for errors:**
   - Go to **"Deployments"** → Click latest → **"View Logs"**
   - Look for any errors

---

## 🚀 Step 12: Upload Products (If Database is Empty)

1. Go to your Railway URL + `/admin/`
2. Login with superuser credentials
3. Add products:
   - Go to **Products** → **Add Product**
   - Fill in details
   - Upload images
   - Save

Or import from Excel:
- Go to **Products** → **Import**
- Select your product Excel file

---

## 🔧 Troubleshooting

### Build Fails

**Check:**
- View build logs in Railway
- Verify `requirements.txt` is correct
- Check `runtime.txt` Python version

**Fix:**
- Railway auto-installs from `requirements.txt`
- Make sure all dependencies are listed

### App Crashes on Startup

**Check logs:**
1. **"Deployments"** → Latest → **"View Logs"**

**Common issues:**
- `SECRET_KEY` not set → Add to Variables
- `ALLOWED_HOSTS` not set → Add to Variables
- Database not connected → Check `DATABASE_URL` is set

**Fix:**
- All environment variables must be set
- Click **"Deploy"** after adding variables

### Static Files Not Loading

**Symptoms:**
- CSS/JS not loading
- Admin panel has no styling

**Fix:**
1. Run collectstatic:
   ```bash
   railway run python manage.py collectstatic --noinput
   ```
2. Or add to build command temporarily

### Images Not Loading (404)

**Problem:** Media files are ephemeral on Railway

**Solutions:**

**Option 1: Railway Volume (Recommended for Demo)**
1. In Railway project → **"+ New"** → **"Volume"**
2. Mount path: `/app/media`
3. Redeploy

**Option 2: Cloud Storage (Recommended for Production)**
- Use AWS S3, Cloudinary, or similar
- Update Django settings to use cloud storage

**Option 3: Commit Sample Images (Quick Fix)**
- Add some sample product images to Git
- They'll be in the deployment

### Database Connection Error

**Check:**
- PostgreSQL service is running
- `DATABASE_URL` is set (should be automatic)

**Fix:**
- Railway sets `DATABASE_URL` automatically
- Don't override it in Variables

### KHQR Payment Not Working

**Check:**
- All Bakong environment variables are set:
  - `BAKONG_ID=vicheka_yeun@wing`
  - `BAKONG_MERCHANT_NAME=MADAM DA`
  - `BAKONG_API_BASE=https://bakongapi.com`

**Test:**
- Visit: `https://your-app.up.railway.app/api/khqr/create/?amount=0.10&currency=USD`
- Should return QR code data (not error)

---

## 📊 Monitor Your Deployment

### View Logs
```bash
railway logs
```

Or in Railway dashboard:
- **"Deployments"** → Click deployment → **"View Logs"**

### View Metrics
- Railway dashboard shows:
  - CPU usage
  - Memory usage
  - Network traffic
  - Request count

---

## 💰 Railway Pricing

### Hobby Plan (Free Tier)
- $5 credit/month (free)
- Sleeps after inactivity
- Perfect for demos
- Wakes up automatically on request

### Paid Plans
- **Developer:** $5/month + usage
- **Team:** $20/month + usage

**For your demo, the free tier is perfect!**

---

## ✅ Final Checklist

Before showing to client:

- [ ] Railway URL works
- [ ] Homepage loads correctly
- [ ] Products display with images
- [ ] Checkout works
- [ ] KHQR payment generates QR codes
- [ ] COD payment works
- [ ] Admin panel accessible
- [ ] Created sample orders for testing
- [ ] Employee dashboard works
- [ ] No errors in logs

---

## 🎉 Success!

Your app is now deployed on Railway!

**Your deployment URL:**
```
https://your-app-name.up.railway.app
```

**Admin panel:**
```
https://your-app-name.up.railway.app/admin/
```

**Employee dashboard:**
```
https://your-app-name.up.railway.app/employee/
```

---

## 🔗 Useful Links

- Railway Dashboard: [railway.app/dashboard](https://railway.app/dashboard)
- Railway Docs: [docs.railway.app](https://docs.railway.app)
- Your GitHub Repo: [github.com/Vicihka/madam-da-show-demo](https://github.com/Vicihka/madam-da-show-demo)

---

## 📞 Need Help?

If you encounter any issues:
1. Check Railway logs first
2. Verify all environment variables are set
3. Check that DATABASE_URL and REDIS_URL are auto-set
4. Make sure migrations ran successfully

**Common fix:** Redeploy after adding/updating environment variables.

---

**Good luck with your client demo! 🚀**

