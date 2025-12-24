# 🔧 Fix Console Errors Guide

## 🐛 Current Errors

1. **Image 404 Error:** `CosrxHya.jpg:1 Failed to load resource: the server responded with a status of 404 (Not Found)`
2. **Bakong API 400 Error:** `api/khqr/create/?amount=0.10&currency=USD:1 Failed to load resource: the server responded with a status of 400 (Bad Request)`

---

## ✅ Fix 1: Image 404 Error

### Problem
The image `CosrxHya.jpg` exists in `media/products/` but the browser can't find it.

### Solutions

#### Solution A: Check Image Path in Database (Most Common)

1. **Go to Django Admin:**
   - Open: `http://127.0.0.1:8000/admin/`
   - Navigate to **Products**

2. **Find the product with `CosrxHya.jpg`:**
   - Search or browse products
   - Click on the product

3. **Check the Image field:**
   - Should show: `products/CosrxHya.jpg` ✅
   - If it shows: `media/products/CosrxHya.jpg` ❌ (wrong!)
   - If it shows: `CosrxHya.jpg` ❌ (wrong!)

4. **Fix if wrong:**
   - Delete the current image
   - Re-upload the image
   - Or manually set to: `products/CosrxHya.jpg`
   - Click **Save**

#### Solution B: Verify File Exists

```bash
# Check if file exists
# Windows PowerShell:
Test-Path "media\products\CosrxHya.jpg"

# Should return: True
```

If file doesn't exist:
1. Copy `CosrxHya.jpg` to `media/products/` folder
2. Update product in Admin to use: `products/CosrxHya.jpg`

#### Solution C: Check DEBUG Mode

**For local development, make sure `DEBUG=True`:**

1. **Check `.env` file:**
   ```env
   DEBUG=True
   ```

2. **Or check `settings.py`:**
   - `DEBUG` should be `True` for development

3. **Restart server:**
   ```bash
   python manage.py runserver
   ```

4. **Test image URL directly:**
   ```
   http://127.0.0.1:8000/media/products/CosrxHya.jpg
   ```
   - Should display the image ✅
   - If 404, check file path in database

#### Solution D: Clear Browser Cache

1. Press `Ctrl + Shift + Delete`
2. Clear cached images and files
3. Or hard refresh: `Ctrl + F5`

---

## ✅ Fix 2: Bakong API 400 Error

### Problem
The Bakong API returns 400 Bad Request when trying to create a payment QR code.

### Root Cause
`BAKONG_ID` is not set in your `.env` file, so it's empty when the API is called.

### Solution: Set BAKONG_ID in .env File

1. **Open or create `.env` file** in project root:
   ```bash
   # Location: D:\Term3 IT STEP\PYTHON\DJANGO - MADAM DA\.env
   ```

2. **Add Bakong configuration:**
   ```env
   # Bakong Payment Configuration
   BAKONG_ID=vicheka_yeun@wing
   BAKONG_MERCHANT_NAME=MADAM DA
   BAKONG_API_BASE=https://bakongapi.com
   ```

3. **Restart Django server:**
   ```bash
   # Stop server (Ctrl+C)
   # Start again:
   python manage.py runserver
   ```

4. **Verify it's loaded:**
   - The error should now show a different message if BAKONG_ID is missing
   - Or test the API endpoint again

### Alternative: Set Environment Variable Directly

**Windows PowerShell:**
```powershell
$env:BAKONG_ID="vicheka_yeun@wing"
$env:BAKONG_MERCHANT_NAME="MADAM DA"
$env:BAKONG_API_BASE="https://bakongapi.com"
```

**Windows CMD:**
```cmd
set BAKONG_ID=vicheka_yeun@wing
set BAKONG_MERCHANT_NAME=MADAM DA
set BAKONG_API_BASE=https://bakongapi.com
```

Then restart server.

---

## 🧪 Test After Fixes

### Test Image Loading

1. **Open browser console** (F12)
2. **Navigate to shop page:**
   ```
   http://127.0.0.1:8000/
   ```
3. **Check console:**
   - Should NOT see 404 errors for images ✅
   - Images should display correctly ✅

### Test Bakong API

1. **Open browser console** (F12)
2. **Go to checkout page:**
   ```
   http://127.0.0.1:8000/checkout/
   ```
3. **Try to create payment:**
   - Add items to cart
   - Proceed to checkout
   - Try to generate payment QR
4. **Check console:**
   - Should NOT see 400 error ✅
   - QR code should generate ✅

### Manual API Test

**Test Bakong API directly:**
```
http://127.0.0.1:8000/api/khqr/create/?amount=0.10&currency=USD
```

**Expected response (if working):**
```json
{
  "error": false,
  "qr_code": "data:image/png;base64,...",
  "md5": "...",
  ...
}
```

**If BAKONG_ID missing:**
```json
{
  "error": true,
  "message": "Bakong ID is not configured. Please set BAKONG_ID in environment variables.",
  "code": "BAKONG_ID_MISSING"
}
```

---

## 📋 Complete .env File Template

Create/update your `.env` file with all required variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,*

# Database (PostgreSQL) - Optional for local (uses SQLite if not set)
DB_NAME=madamda_db
DB_USER=postgres
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=5432

# Redis - Optional for local
REDIS_URL=redis://127.0.0.1:6379/1

# Telegram Bot (Optional)
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here
TELEGRAM_CHAT_ID=your-telegram-chat-id-here

# Bakong Payment (REQUIRED for payment to work)
BAKONG_ID=vicheka_yeun@wing
BAKONG_MERCHANT_NAME=MADAM DA
BAKONG_API_BASE=https://bakongapi.com

# SSL/HTTPS (Production Only)
ENABLE_SSL_REDIRECT=False
```

---

## ✅ Quick Fix Checklist

**For Image 404 Error:**
- [ ] Check product image path in Admin (should be `products/filename.jpg`)
- [ ] Verify file exists in `media/products/` folder
- [ ] Ensure `DEBUG=True` in `.env`
- [ ] Restart Django server
- [ ] Clear browser cache (Ctrl+F5)
- [ ] Test image URL directly: `http://127.0.0.1:8000/media/products/CosrxHya.jpg`

**For Bakong API 400 Error:**
- [ ] Create/update `.env` file in project root
- [ ] Add `BAKONG_ID=vicheka_yeun@wing`
- [ ] Add `BAKONG_MERCHANT_NAME=MADAM DA`
- [ ] Add `BAKONG_API_BASE=https://bakongapi.com`
- [ ] Restart Django server
- [ ] Test API endpoint again

---

## 🔍 Still Having Issues?

### Image Still Not Loading

1. **Check server logs:**
   - Look for errors in terminal where server is running
   - Check for file permission errors

2. **Verify MEDIA settings:**
   ```python
   # In project/settings.py:
   MEDIA_URL = 'media/'
   MEDIA_ROOT = BASE_DIR / 'media'
   ```

3. **Check URL configuration:**
   ```python
   # In project/urls.py (should be there):
   if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```

### Bakong API Still Failing

1. **Verify BAKONG_ID is loaded:**
   - Add this to a view temporarily to check:
   ```python
   from project.settings import BAKONG_ID
   print(f"BAKONG_ID: {BAKONG_ID}")
   ```

2. **Check Bakong API response:**
   - Open Network tab in browser (F12)
   - Check the actual error message from API
   - Might be 403 Forbidden (wrong credentials)
   - Might be 400 Bad Request (missing/invalid parameters)

3. **Test with curl or Postman:**
   ```bash
   curl "http://127.0.0.1:8000/api/khqr/create/?amount=0.10&currency=USD"
   ```

---

## 📚 Related Guides

- **Image Setup:** See `IMAGE_SETUP_GUIDE.md`
- **Bakong Configuration:** See `BAKONG_CONFIGURATION.md`
- **Railway Deployment:** See `RAILWAY_DEPLOYMENT_GUIDE.md`

---

## 🎯 Summary

**Image Error Fix:**
1. Check image path in Admin → Products
2. Should be: `products/CosrxHya.jpg`
3. Ensure `DEBUG=True`
4. Restart server

**Bakong Error Fix:**
1. Create `.env` file
2. Add `BAKONG_ID=vicheka_yeun@wing`
3. Restart server

**Both errors should now be fixed!** ✅

