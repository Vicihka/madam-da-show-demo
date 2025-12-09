# 📦 Storage Structures Report - MADAM DA Website

**Date:** December 7, 2025  
**Project:** MADAM DA E-Commerce Platform

---

## 📊 **Overview**

Your website uses **multiple storage systems** to handle different types of data:

1. **Database Storage** (PostgreSQL/SQLite) - Structured data
2. **File Storage** (Media Files) - Images, videos, QR codes
3. **Static Files** - CSS, JavaScript, images
4. **Session Storage** - User sessions
5. **Cache Storage** - Performance optimization
6. **Log Files** - Error tracking and debugging

---

## 🗄️ **1. DATABASE STORAGE**

### **Database Type:**
- **Development:** SQLite (`db.sqlite3`)
- **Production:** PostgreSQL (configurable via environment variables)

### **Database Models & Storage:**

#### **A. Product Model** (`app/models.py`)
```python
- id: CharField (Primary Key)
- name: CharField (200 chars)
- name_kh: CharField (200 chars) - Khmer name
- description: TextField
- description_kh: TextField - Khmer description
- price: DecimalField (10 digits, 2 decimals)
- old_price: DecimalField (10 digits, 2 decimals)
- image: ImageField → Stored in: media/products/
- badge: CharField (50 chars)
- badge_kh: CharField (50 chars)
- stock: IntegerField
- is_active: BooleanField
- created_at: DateTimeField
- updated_at: DateTimeField
```

**Storage Location:** `media/products/`  
**File Size Limit:** 5MB per image  
**Allowed Formats:** JPG, JPEG, PNG, WebP, GIF

---

#### **B. Customer Model**
```python
- id: UUIDField (Primary Key, auto-generated)
- name: CharField (200 chars)
- phone: CharField (20 chars) - UNIQUE INDEX
- email: EmailField
- address: TextField
- province: CharField (100 chars)
- loyalty_points: IntegerField (default: 0)
- referral_code: CharField (20 chars) - UNIQUE
- referred_by: ForeignKey (self-reference)
- created_at: DateTimeField
- updated_at: DateTimeField - INDEXED
```

**Indexes:**
- `phone` - Unique index for fast lookup
- `updated_at` - Index for recent customer queries

---

#### **C. Order Model** (Main Order Data)
```python
- order_number: CharField (20 chars) - UNIQUE
- customer: ForeignKey (Customer)
- customer_name: CharField (200 chars)
- customer_phone: CharField (20 chars) - INDEXED
- customer_email: EmailField
- customer_address: TextField
- customer_province: CharField (100 chars)
- subtotal: DecimalField (10 digits, 2 decimals)
- shipping_fee: DecimalField (10 digits, 2 decimals)
- discount_amount: DecimalField (10 digits, 2 decimals)
- total: DecimalField (10 digits, 2 decimals)
- payment_method: CharField (50 chars)
- status: CharField (20 chars) - INDEXED
- promo_code: ForeignKey (PromoCode)
- loyalty_points_used: IntegerField
- loyalty_points_earned: IntegerField
- referral_code_used: CharField (20 chars)
- notes: TextField
- payment_received: BooleanField - INDEXED
- payment_received_at: DateTimeField
- payment_received_by: CharField (200 chars)
- cod_delivery_notes: TextField
- is_verified: BooleanField
- verification_status: CharField (20 chars)
- verification_notes: TextField
- verified_by: CharField (200 chars)
- verified_at: DateTimeField
- is_suspicious: BooleanField
- suspicious_reason: CharField (500 chars)
- customer_received: BooleanField - INDEXED
- customer_received_at: DateTimeField
- customer_received_by: CharField (200 chars)
- customer_received_notes: TextField
- created_at: DateTimeField - INDEXED
- updated_at: DateTimeField
```

**Indexes (Performance Optimization):**
- `customer_phone` - Fast customer order lookup
- `status` - Fast status filtering
- `created_at` - Fast date sorting
- `payment_received` - Fast COD payment queries
- `customer_received` - Fast delivery tracking
- **Composite Indexes:**
  - `(status, created_at)` - Dashboard queries
  - `(customer_phone, created_at)` - Customer order history
  - `(status, payment_method, payment_received)` - Payment filtering
  - `(status, customer_received, customer_received_at)` - Delivery queries

---

#### **D. OrderItem Model**
```python
- order: ForeignKey (Order)
- product: ForeignKey (Product)
- product_name: CharField (200 chars)
- product_price: DecimalField (10 digits, 2 decimals)
- quantity: IntegerField
- subtotal: DecimalField (10 digits, 2 decimals)
```

---

#### **E. OrderQRCode Model** (KHQR Payment QR Codes)
```python
- order: OneToOneField (Order)
- qr_code_image: ImageField → Stored in: media/qr_codes/
- qr_data: TextField
- created_at: DateTimeField
- expires_at: DateTimeField (5 minutes after creation)
- is_used: BooleanField
- used_at: DateTimeField
```

**Storage Location:** `media/qr_codes/`  
**File Format:** PNG  
**Expiration:** 5 minutes after creation

---

#### **F. HeroSlide Model** (Homepage Carousel)
```python
- title: CharField (200 chars)
- subtitle: CharField (300 chars)
- slide_type: CharField (10 chars) - 'image', 'video', 'url'
- image: ImageField → Stored in: media/hero_slides/
- video: FileField → Stored in: media/hero_slides/videos/
- external_url: URLField
- order: IntegerField
- is_active: BooleanField
- created_at: DateTimeField
- updated_at: DateTimeField
```

**Storage Locations:**
- Images: `media/hero_slides/`
- Videos: `media/hero_slides/videos/`
**File Size Limits:**
- Images: 5MB max
- Videos: 50MB max
**Allowed Formats:**
- Images: JPG, JPEG, PNG, WebP, GIF
- Videos: MP4, WebM, MOV

---

#### **G. PromoCode Model**
```python
- code: CharField (50 chars) - UNIQUE
- promoter: ForeignKey (Promoter)
- description: CharField (200 chars)
- description_kh: CharField (200 chars)
- discount_type: CharField (20 chars) - 'percentage' or 'fixed'
- discount_value: DecimalField (10 digits, 2 decimals)
- min_purchase: DecimalField (10 digits, 2 decimals)
- max_discount: DecimalField (10 digits, 2 decimals)
- usage_limit: IntegerField
- used_count: IntegerField
- is_active: BooleanField
- valid_from: DateTimeField
- valid_until: DateTimeField
- created_at: DateTimeField
- updated_at: DateTimeField
```

---

#### **H. Promoter Model**
```python
- name: CharField (200 chars)
- phone: CharField (20 chars)
- email: EmailField
- commission_rate: DecimalField (5 digits, 2 decimals)
- is_active: BooleanField
- notes: TextField
- created_at: DateTimeField
- updated_at: DateTimeField
```

---

#### **I. Newsletter Model**
```python
- email: EmailField - UNIQUE
- name: CharField (200 chars)
- phone: CharField (20 chars)
- is_active: BooleanField
- subscribed_at: DateTimeField
- unsubscribed_at: DateTimeField
```

---

#### **J. Referral Model**
```python
- referrer: ForeignKey (Customer)
- referred_customer: ForeignKey (Customer)
- referral_code: CharField (20 chars)
- reward_points: IntegerField
- is_rewarded: BooleanField
- created_at: DateTimeField
```

---

#### **K. LoyaltyPoint Model**
```python
- customer: ForeignKey (Customer)
- points: IntegerField
- transaction_type: CharField (20 chars) - 'earned', 'used', 'expired', 'bonus'
- description: CharField (200 chars)
- order: ForeignKey (Order)
- expires_at: DateTimeField
- created_at: DateTimeField
```

---

## 📁 **2. FILE STORAGE (MEDIA FILES)**

### **Media Root:** `BASE_DIR / 'media'`

### **Storage Structure:**
```
media/
├── products/              # Product images
│   └── COSRXVitaminC23.jpg
├── hero_slides/           # Homepage carousel
│   ├── 220938c609a7a3995729b8bf118a8c43.jpg
│   └── videos/           # Hero slide videos
│       └── (video files)
└── qr_codes/            # QR code images
    ├── qr_MD00001.png    # KHQR payment QR codes
    ├── qr_MD00033.png
    ├── tracking_qr_MD00031.png  # Order tracking QR codes
    └── ... (many more)
```

### **Current Storage:**
- **Product Images:** 1 file
- **Hero Slides:** 1 image
- **QR Codes:** 28 files (payment + tracking)

### **File Upload Settings:**
- **Max Image Size:** 5MB
- **Max Video Size:** 50MB
- **Storage Backend:** Django's default file storage
- **URL Path:** `/media/`

---

## 🎨 **3. STATIC FILES**

### **Static Root:** `BASE_DIR / 'staticfiles'` (production)  
### **Static Source:** `BASE_DIR / 'static'` (development)

### **Storage Structure:**
```
static/
├── images/
│   ├── favicon.png
│   ├── jandt-logo.png
│   └── madam-da-logo.png
└── js/
    ├── html5-qrcode.min.js
    └── qrcode.min.js
```

### **Static Files Settings:**
- **STATIC_URL:** `/static/`
- **STATICFILES_DIRS:** `[BASE_DIR / 'static']`
- **STATIC_ROOT:** `BASE_DIR / 'staticfiles'`
- **Storage Backend:** `ManifestStaticFilesStorage` (with cache busting)
- **Cache Duration:** 1 year (31536000 seconds)

---

## 🍪 **4. SESSION STORAGE**

### **Session Engine:**
- **Development:** Database-backed sessions
- **Production:** Cache-backed sessions (Redis)

### **Session Settings:**
```python
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'  # Production
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = not DEBUG  # Secure in production
```

### **Storage Location:**
- **Development:** Database (SQLite/PostgreSQL)
- **Production:** Redis cache

---

## ⚡ **5. CACHE STORAGE**

### **Cache Backend:**
- **Development:** Dummy cache (no actual caching)
- **Production:** Redis cache

### **Cache Configuration:**
```python
# Development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Production
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            'IGNORE_EXCEPTIONS': True,
        },
        'KEY_PREFIX': 'madamda',
        'TIMEOUT': 300,  # 5 minutes
    }
}
```

### **Cache Usage:**
- Session storage
- Rate limiting
- Static file caching
- Query result caching (if implemented)

---

## 📝 **6. LOG FILES**

### **Log Directory:** `BASE_DIR / 'logs'`

### **Log Files:**
```
logs/
├── django.log        # General application logs
└── security.log     # Security-related logs
```

### **Log Configuration:**
- **Log Level:** WARNING (django), INFO (app)
- **Log Format:** Verbose with timestamps
- **Rotation:** Manual (file-based)

---

## 🔍 **7. DATABASE INDEXES (Performance)**

### **Indexes on Order Model:**
1. `customer_phone` - Fast customer order lookup
2. `status` - Fast status filtering
3. `created_at` - Fast date sorting
4. `payment_received` - Fast COD payment queries
5. `customer_received` - Fast delivery tracking
6. **Composite:** `(status, created_at)` - Dashboard queries
7. **Composite:** `(customer_phone, created_at)` - Customer history
8. **Composite:** `(status, payment_method, payment_received)` - Payment filtering
9. **Composite:** `(status, customer_received, customer_received_at)` - Delivery queries

### **Indexes on Customer Model:**
1. `phone` - Unique index (fast lookup)
2. `updated_at` - Recent customer queries

---

## 📊 **8. STORAGE SUMMARY**

### **Database Tables:**
- **11 Models** storing structured data
- **Primary Storage:** PostgreSQL (production) or SQLite (development)

### **File Storage:**
- **Media Files:** ~30 files (products, hero slides, QR codes)
- **Static Files:** ~5 files (images, JavaScript)
- **Total Estimated Size:** < 50MB

### **Session Storage:**
- **Location:** Redis (production) or Database (development)
- **Lifetime:** 1 hour
- **Auto-expire:** Yes (on browser close)

### **Cache Storage:**
- **Backend:** Redis (production) or Dummy (development)
- **Timeout:** 5 minutes
- **Compression:** Enabled (zlib)

---

## 🚀 **9. STORAGE OPTIMIZATION**

### **Current Optimizations:**
1. ✅ **Database Indexes** - Fast queries
2. ✅ **File Validation** - Size and type limits
3. ✅ **Static File Caching** - 1 year cache
4. ✅ **Cache Compression** - Reduced memory usage
5. ✅ **Session Expiration** - Automatic cleanup

### **Recommendations:**
1. **Image Optimization:** Use WebP format for smaller file sizes
2. **QR Code Cleanup:** Remove expired QR codes (> 5 minutes old)
3. **Log Rotation:** Implement automatic log rotation
4. **Media Backup:** Regular backups of media files
5. **Database Backup:** Regular database backups

---

## 📈 **10. STORAGE GROWTH ESTIMATES**

### **Per Order:**
- **Database:** ~2-5 KB (order + items + QR code record)
- **Files:** ~50-100 KB (QR code image)

### **Per Product:**
- **Database:** ~1-2 KB
- **Files:** ~100-500 KB (product image)

### **Monthly Growth (100 orders/month):**
- **Database:** ~200-500 KB
- **Files:** ~5-10 MB (QR codes)

### **Yearly Growth (1200 orders/year):**
- **Database:** ~2.4-6 MB
- **Files:** ~60-120 MB (QR codes)

---

## ✅ **11. STORAGE HEALTH CHECK**

### **Current Status:**
- ✅ Database indexes properly configured
- ✅ File upload limits enforced
- ✅ Session storage configured
- ✅ Cache storage configured (production)
- ✅ Log files directory exists
- ✅ Media files organized by type

### **Action Items:**
- [ ] Implement QR code cleanup (remove expired codes)
- [ ] Set up automatic log rotation
- [ ] Configure database backups
- [ ] Monitor storage growth
- [ ] Optimize product images (convert to WebP)

---

## 📋 **12. STORAGE CONFIGURATION FILES**

### **Settings File:** `project/settings.py`
- Media URL: `MEDIA_URL = 'media/'`
- Media Root: `MEDIA_ROOT = BASE_DIR / 'media'`
- Static URL: `STATIC_URL = 'static/'`
- Static Root: `STATIC_ROOT = BASE_DIR / 'staticfiles'`

### **Models File:** `app/models.py`
- All model definitions with field types
- File upload paths (`upload_to` parameters)
- Validation functions

---

## 🎯 **Conclusion**

Your website has a **well-organized storage structure** with:
- ✅ Proper database indexing for performance
- ✅ Organized file storage (media/static separation)
- ✅ Session and cache management
- ✅ Logging for debugging
- ✅ File validation and size limits

**Storage is efficient and scalable** for your current needs. Consider implementing cleanup routines for expired QR codes and log rotation for long-term maintenance.

---

**Report Generated:** December 7, 2025  
**Next Review:** When storage exceeds 1GB or after 1000 orders

