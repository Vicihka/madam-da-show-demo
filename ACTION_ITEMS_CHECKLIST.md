# ✅ Action Items Checklist
**Created:** December 18, 2025  
**Status:** Ready to Execute

This is your prioritized checklist based on the comprehensive audit.

---

## 🔴 CRITICAL - Do First (Required for Basic Functionality)

### [ ] 1. Create Track Order Template
**Why:** URL exists but template is missing - will cause 404 error

**What to do:**
```bash
# Create this file:
touch "templates/app/shop/track_order.html"
```

**Template should include:**
- Form with phone number + order number inputs
- Display order status after submission
- Show order items and timeline
- Use similar styling to order_success.html

**Files to reference:**
- `templates/app/shop/order_success.html` - For styling
- `templates/app/shop/checkout.html` - For form structure
- `app/views.py` - `track_order_view()` function (already exists)

**Time estimate:** 30-60 minutes

---

## 🟡 HIGH PRIORITY - Do Next (Improve User Experience)

### [ ] 2. Implement Delivery Note Feature
**Why:** Field exists but value is never saved

**Files to modify:**

#### A. Frontend (`static/shop/js/checkout.js`)
Find where order data is collected and add:
```javascript
// Get delivery note value
const deliveryNote = document.getElementById('delivery-note').value;

// Add to orderData object:
orderData.delivery_note = deliveryNote;
```

#### B. Backend (`app/views.py`)
In `create_order_on_payment()` function, add:
```python
# Save delivery note
order.notes = request.POST.get('delivery_note', '')
order.save()
```

**Time estimate:** 20-30 minutes

---

### [ ] 3. Implement Telegram Toggle Feature
**Why:** Toggle exists but state is ignored (always sends notification)

**Files to modify:**

#### A. Frontend (`static/shop/js/checkout.js`)
Add telegram toggle state to order data:
```javascript
// Get telegram toggle state
const telegramToggle = document.getElementById('telegram-toggle');
const notifyViaTelegram = telegramToggle.dataset.state === 'checked';

// Add to orderData object:
orderData.notify_via_telegram = notifyViaTelegram;
```

#### B. Backend (`app/views.py`)
In `create_order_on_payment()` and COD creation, add:
```python
# Check if should notify via Telegram
notify_telegram = request.POST.get('notify_via_telegram', 'true') == 'true'

# Conditionally send notification
if notify_telegram and settings.TELEGRAM_ENABLED:
    send_telegram_notification(order)
```

**Time estimate:** 30-40 minutes

---

## 🟢 CLEANUP - Do When You Can (Nice to Have)

### [ ] 4. Delete Old Employee Dashboard
**Why:** Duplicate file causes confusion

```bash
# Delete the old file
rm "templates/app/employee_dashboard.html"
```

**Time estimate:** 1 minute

---

### [ ] 5. Create .env File
**Why:** Need proper configuration for production

```bash
# Copy template
cp ENV_TEMPLATE.txt .env

# Edit and configure:
# - SECRET_KEY (generate new for production)
# - DEBUG=False (for production)
# - ALLOWED_HOSTS (your domain)
# - TELEGRAM_BOT_TOKEN (if using)
# - BAKONG_ID (if using)

# IMPORTANT: Verify .env is in .gitignore!
```

**Time estimate:** 10 minutes

---

### [ ] 6. Decide on Employee Static Folders
**Why:** Empty folders exist

**Option A:** Use them
- Move employee dashboard styles to `static/employee/css/`
- Move employee dashboard scripts to `static/employee/js/`

**Option B:** Delete them
```bash
rmdir static/employee/css
rmdir static/employee/js
rmdir static/employee
```

**Time estimate:** 5 minutes

---

## 🧪 TESTING - After Completing Above

### [ ] 7. Test Complete Purchase Flow
**KHQR Payment:**
- [ ] Add products to cart
- [ ] Go to checkout
- [ ] Fill in customer details
- [ ] Add delivery note
- [ ] Toggle Telegram notification
- [ ] Select KHQR payment
- [ ] Generate QR code
- [ ] Verify order created
- [ ] Check admin panel
- [ ] Verify Telegram notification (if enabled)

**COD Payment:**
- [ ] Add products to cart
- [ ] Go to checkout
- [ ] Fill in customer details
- [ ] Add delivery note
- [ ] Toggle Telegram notification OFF
- [ ] Select COD
- [ ] Complete order
- [ ] Verify COD QR code generated
- [ ] Verify NO Telegram notification sent

### [ ] 8. Test Order Tracking
- [ ] Go to /track-order/
- [ ] Enter phone number + order number
- [ ] Verify order displays correctly
- [ ] Check order status shows properly

### [ ] 9. Test Employee Dashboard
- [ ] Open employee dashboard
- [ ] Create new order (from customer side)
- [ ] Verify real-time notification appears
- [ ] Update order status
- [ ] Confirm COD payment
- [ ] Print QR code

### [ ] 10. Test on Mobile
- [ ] Test on actual mobile device
- [ ] Check responsiveness
- [ ] Test touch interactions
- [ ] Test QR code scanning

---

## 📋 PRODUCTION PREP - Before Launch

### [ ] 11. Security Configuration
- [ ] Set `DEBUG=False`
- [ ] Set strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set `ENABLE_SSL_REDIRECT=True` (if HTTPS)
- [ ] Configure `CSRF_TRUSTED_ORIGINS`

### [ ] 12. Database Setup
- [ ] Set up PostgreSQL (if using)
- [ ] Run migrations
- [ ] Create superuser
- [ ] Load initial data

### [ ] 13. Redis Setup
- [ ] Install Redis
- [ ] Start Redis service
- [ ] Test WebSocket connection

### [ ] 14. Static Files
- [ ] Run `python manage.py collectstatic`
- [ ] Verify static files serve correctly

### [ ] 15. External Services
- [ ] Configure Telegram bot token
- [ ] Configure Bakong KHQR credentials
- [ ] Test payment integration

---

## 📊 Progress Tracker

**Completed:** 5/15 items ✅
**In Progress:** 0/15 items
**Remaining:** 10/15 items

**Estimated Total Time:** 
- Critical items: 1-2 hours
- High priority: 1-2 hours
- Cleanup: 30 minutes
- Testing: 2-3 hours
- Production prep: 2-4 hours
- **Total: 7-12 hours of work**

---

## 🎯 Quick Start Path

**If you want to launch ASAP, do this minimum:**

1. ✅ Create track_order.html (30 min)
2. ✅ Test order tracking works (10 min)
3. ✅ Create .env file (10 min)
4. ✅ Test full purchase flow (30 min)
5. ✅ Production configuration (1 hour)
6. ✅ Deploy

**Minimum viable launch:** 2-3 hours

---

## 💡 Tips

1. **Work in order** - Critical items first
2. **Test after each change** - Don't wait until the end
3. **Commit frequently** - Git is your friend
4. **Keep backups** - Before making big changes
5. **Read the docs** - You have excellent documentation!

---

## 📞 Need Help?

**Reference these files:**
- `COMPREHENSIVE_PROJECT_AUDIT.md` - Full analysis
- `PROJECT_OVERVIEW.md` - Feature overview
- `pre_deployment/` folder - Deployment guides
- `CHECKOUT_NOTE_AND_TELEGRAM_EXPLANATION.md` - Delivery note details

---

**Last Updated:** December 18, 2025  
**Next Review:** After completing critical items

Good luck! 🚀

