# 💳 Bakong Payment Configuration

## ✅ Configuration Complete

Your Bakong payment integration is now configured with:

- **BAKONG_ID:** `vicheka_yeun@wing`
- **BAKONG_MERCHANT_NAME:** `MADAM DA`
- **BAKONG_API_BASE:** `https://bakongapi.com`

---

## 🔧 Local Development Setup

### Update Your `.env` File

Add these lines to your `.env` file (create it if it doesn't exist):

```env
# Bakong Payment Configuration
BAKONG_ID=vicheka_yeun@wing
BAKONG_MERCHANT_NAME=MADAM DA
BAKONG_API_BASE=https://bakongapi.com
```

**Note:** `.env` is already in `.gitignore`, so it won't be committed to GitHub.

---

## 🚂 Railway Deployment

### Environment Variables to Set

When deploying to Railway, add these environment variables in the Railway dashboard:

1. Go to your service → **"Variables"** tab
2. Add the following:

```env
BAKONG_ID=vicheka_yeun@wing
BAKONG_MERCHANT_NAME=MADAM DA
BAKONG_API_BASE=https://bakongapi.com
```

---

## ✅ How It Works

Your application uses Bakong API for:

1. **Creating KHQR Payment Codes** (`/create_khqr/`)
   - Generates QR codes for customers to scan and pay
   - Supports USD and KHR currencies
   - Minimum amount: $0.10 USD or 400 KHR

2. **Checking Payment Status** (`/check_payment/`)
   - Verifies if payment has been completed
   - Uses MD5 hash from the QR code

---

## 🧪 Testing

### Test Payment Flow

1. **Create a test order** in your application
2. **Generate KHQR code** - Should return a QR code image
3. **Scan with Bakong app** - Use your Bakong mobile app
4. **Check payment status** - Verify payment is detected

### API Endpoints

- **Create QR Code:**
  ```
  GET /create_khqr/?amount=10.00&currency=USD
  ```

- **Check Payment:**
  ```
  GET /check_payment/?md5=<md5_hash_from_qr>
  ```

---

## ⚠️ Important Notes

1. **Merchant Name Must Match:** 
   - `BAKONG_MERCHANT_NAME` must match exactly what's in your Bakong dashboard whitelist
   - Current value: `MADAM DA`

2. **Bakong ID Format:**
   - Your Bakong ID: `vicheka_yeun@wing`
   - This should be your registered Bakong account

3. **API Base URL:**
   - Default: `https://bakongapi.com`
   - Don't change unless Bakong provides a different endpoint

4. **Error Handling:**
   - If you get 403 Forbidden, check:
     - Bakong ID is correct
     - Merchant name matches exactly
     - Account is properly configured in Bakong dashboard

---

## 🔍 Troubleshooting

### Payment QR Code Not Generating

**Check:**
- [ ] `BAKONG_ID` is set correctly
- [ ] `BAKONG_MERCHANT_NAME` matches Bakong dashboard
- [ ] Amount meets minimum requirements ($0.10 USD or 400 KHR)
- [ ] Check Railway logs for API errors

### Payment Status Not Updating

**Check:**
- [ ] MD5 hash is correct (32 characters)
- [ ] Using the same `BAKONG_ID` for both create and check
- [ ] Payment was actually completed in Bakong app
- [ ] API is responding (check logs)

### 403 Forbidden Error

**Solutions:**
1. Verify `BAKONG_ID` is correct: `vicheka_yeun@wing`
2. Verify `BAKONG_MERCHANT_NAME` matches exactly: `MADAM DA`
3. Check Bakong dashboard for account status
4. Ensure account is whitelisted for API access

---

## 📚 Related Files

- **Settings:** `project/settings.py` (lines 472-475)
- **Views:** `app/views.py` (create_khqr, check_payment functions)
- **Environment Template:** `ENV_TEMPLATE.txt`
- **Railway Guides:** `RAILWAY_DEPLOYMENT_GUIDE.md`, `RAILWAY_QUICK_START.md`

---

## ✅ Configuration Status

- ✅ Bakong ID configured: `vicheka_yeun@wing`
- ✅ Merchant name set: `MADAM DA`
- ✅ API base URL configured
- ✅ Environment variable support in settings
- ✅ Railway deployment guides updated

**Your Bakong payment integration is ready to use!** 💳

