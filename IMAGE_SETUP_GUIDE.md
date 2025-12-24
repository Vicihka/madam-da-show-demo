# 🖼️ Image Setup Guide for MADAM DA

## ✅ Current Status

Your images are stored in: `media/products/`

**Found images:**
- ✅ `CosrxHya.jpg` (exists in media/products/)
- ✅ `COSRXVitaminC23.jpg`
- ✅ `COSRXVitaminC23_800x.webp`
- ✅ Other product images

---

## 🔧 How to Set/Upload Product Images

### Method 1: Django Admin Panel (Recommended)

1. **Access Admin Panel:**
   - Go to: `http://127.0.0.1:8000/admin/`
   - Login with your superuser account

2. **Add/Edit Product:**
   - Go to **"Products"** section
   - Click on a product to edit, or **"Add Product"** to create new
   - In the **"Media"** section, click **"Choose File"** under **"Image"**
   - Select your image file (JPG, PNG, WEBP, GIF)
   - Click **"Save"**

3. **Image Requirements:**
   - Formats: JPG, JPEG, PNG, WEBP, GIF
   - Recommended size: 800x800px or larger
   - Max file size: 5MB (configured in settings)

### Method 2: Upload via File System

1. **Place image in media folder:**
   ```bash
   # Copy your image to:
   media/products/your-image-name.jpg
   ```

2. **Update Product in Admin:**
   - Go to Admin → Products
   - Edit the product
   - Set image field to: `products/your-image-name.jpg`
   - Save

### Method 3: Import via Excel/CSV

1. **Prepare Excel file:**
   - Include column: `image` with path like `products/image-name.jpg`
   - Make sure images are in `media/products/` folder

2. **Import in Admin:**
   - Go to Admin → Products
   - Click **"Import"**
   - Select your Excel file
   - Click **"Submit"**

---

## 🐛 Fixing Image 404 Errors

### Issue: Images Not Loading (404 Error)

**Problem:** Browser shows `404 Not Found` for images like `CosrxHya.jpg`

**Solutions:**

#### 1. Check Media URL Configuration

Your `project/urls.py` should serve media files in development:

```python
# This is already configured in your project/urls.py (lines 92-94)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**Verify:**
- `DEBUG=True` in your `.env` file or settings
- Server is running with `python manage.py runserver`

#### 2. Check Image Path in Database

The image path in the database should be relative to `MEDIA_ROOT`:

**Correct format:**
- `products/CosrxHya.jpg` ✅
- `media/products/CosrxHya.jpg` ❌ (wrong - don't include "media/")

**To check/fix:**
1. Go to Admin → Products
2. Check the product's image field
3. Should show: `products/CosrxHya.jpg`
4. If it shows full path, edit and correct it

#### 3. Verify File Exists

```bash
# Check if file exists
ls media/products/CosrxHya.jpg

# Or in Windows PowerShell:
Test-Path "media\products\CosrxHya.jpg"
```

#### 4. Check MEDIA_URL and MEDIA_ROOT Settings

In `project/settings.py` (already configured correctly):

```python
MEDIA_URL = 'media/'  # URL prefix
MEDIA_ROOT = BASE_DIR / 'media'  # File system path
```

**Image URL will be:** `http://127.0.0.1:8000/media/products/CosrxHya.jpg`

---

## 🚂 For Railway Deployment

### Important: Media Files on Railway

⚠️ **Railway's filesystem is ephemeral** - uploaded files are lost on redeploy!

**Solutions:**

#### Option 1: Use Cloud Storage (Recommended for Production)

1. **Install django-storages:**
   ```bash
   pip install django-storages boto3
   ```

2. **Configure AWS S3 or Cloudinary:**
   - Update `settings.py` to use cloud storage
   - Images will persist across deployments

#### Option 2: Use Railway Volume (For Demo)

1. **Add Railway Volume:**
   - In Railway dashboard → Add Volume
   - Mount to `/app/media`
   - Files will persist

#### Option 3: Commit Images to Git (Not Recommended)

⚠️ **Only for small demos:**
- Add images to `media/products/`
- Commit to Git
- Images will be in repository
- **Note:** Large files will slow down Git

**For your demo, Option 2 (Volume) is easiest!**

---

## 📝 Step-by-Step: Fix Current Image Issue

### Step 1: Check Product in Database

1. Go to Admin → Products
2. Find product with missing image
3. Check the **"Image"** field value
4. Should be: `products/CosrxHya.jpg`

### Step 2: Verify File Location

```bash
# File should be at:
media/products/CosrxHya.jpg
```

### Step 3: Check Server is Serving Media

1. Make sure `DEBUG=True` in `.env`:
   ```env
   DEBUG=True
   ```

2. Restart server:
   ```bash
   python manage.py runserver
   ```

3. Test image URL directly:
   ```
   http://127.0.0.1:8000/media/products/CosrxHya.jpg
   ```

### Step 4: Re-upload Image (If Still Not Working)

1. Go to Admin → Products
2. Edit the product
3. Delete current image
4. Upload image again
5. Save

---

## 🔍 Troubleshooting

### Image Shows in Admin but Not on Website

**Check:**
- [ ] Image path in database is correct (`products/filename.jpg`)
- [ ] File exists in `media/products/`
- [ ] `DEBUG=True` (for development)
- [ ] Server restarted after changes
- [ ] Browser cache cleared (Ctrl+F5)

### Image Upload Fails

**Check:**
- [ ] File size < 5MB
- [ ] File format is JPG, PNG, WEBP, or GIF
- [ ] `media/products/` folder exists and is writable
- [ ] Check server logs for errors

### Images Work Locally but Not on Railway

**Solutions:**
1. Use Railway Volume for media files
2. Or switch to cloud storage (S3, Cloudinary)
3. Or commit images to Git (small demos only)

---

## ✅ Quick Checklist

**For Local Development:**
- [ ] `DEBUG=True` in `.env`
- [ ] Images in `media/products/` folder
- [ ] Image path in database: `products/filename.jpg`
- [ ] Server running: `python manage.py runserver`
- [ ] Test URL: `http://127.0.0.1:8000/media/products/filename.jpg`

**For Railway Deployment:**
- [ ] Add Railway Volume for media files
- [ ] OR use cloud storage (S3/Cloudinary)
- [ ] Update `MEDIA_ROOT` if using volume
- [ ] Test image URLs after deployment

---

## 📚 Related Files

- **Settings:** `project/settings.py` (lines 331-333)
- **URLs:** `project/urls.py` (lines 92-94)
- **Model:** `app/models.py` (Product model, line 52-56)
- **Admin:** `app/admin.py` (ProductAdmin, line 100-103)

---

## 🎯 Next Steps

1. **Fix current 404 error:**
   - Check product in Admin
   - Verify image path
   - Re-upload if needed

2. **For Railway:**
   - Set up Railway Volume
   - Or configure cloud storage

3. **Test:**
   - Verify images load on website
   - Test on mobile device
   - Check after Railway deployment

**Your images should now work correctly!** 🖼️

