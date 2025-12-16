# 🔍 Pre-Deployment Testing Checklist - MADAM DA E-Commerce

**Last Updated:** 2024-01-15  
**Status:** Ready for Production Testing

---

## 📋 Table of Contents

1. [Complete Testing Checklist](#complete-testing-checklist)
2. [Payment Processing Testing](#payment-processing-testing)
3. [User Authentication & Registration Testing](#user-authentication--registration-testing)
4. [Admin Panel Testing](#admin-panel-testing)
5. [Form Validation Testing](#form-validation-testing)
6. [Mobile Responsiveness Testing](#mobile-responsiveness-testing)
7. [Performance Testing](#performance-testing)
8. [Security Testing](#security-testing)

---

## ✅ Complete Testing Checklist

### 🛒 **Product & Shopping Features**

#### Product Display
- [ ] **Homepage loads correctly**
  - [ ] Products display with images
  - [ ] Product names and prices show correctly
  - [ ] Khmer text displays properly (if applicable)
  - [ ] Hero slides/carousel works
  - [ ] Pagination works (if >20 products)
  - [ ] Out-of-stock products handled correctly

- [ ] **Product Details**
  - [ ] Product images load
  - [ ] Prices formatted correctly
  - [ ] Stock status accurate
  - [ ] Add to cart button works
  - [ ] Cannot add out-of-stock items to cart

#### Shopping Cart
- [ ] **Cart Functionality**
  - [ ] Add product to cart
  - [ ] Update cart quantity
  - [ ] Remove item from cart
  - [ ] Cart persists across page reloads (localStorage)
  - [ ] Cart count badge updates
  - [ ] Empty cart state handled
  - [ ] Cart totals calculate correctly
  - [ ] Multiple products in cart work

---

### 💳 **Checkout & Payment**

#### Checkout Form
- [ ] **Form Validation**
  - [ ] Name field required
  - [ ] Phone field required (format validation)
  - [ ] Address field required
  - [ ] Province selection required
  - [ ] Cannot submit empty form
  - [ ] Error messages display correctly
  - [ ] Form resets after successful order

- [ ] **Checkout Flow**
  - [ ] Customer information loads if exists
  - [ ] Form pre-fills for returning customers
  - [ ] Cart items display correctly
  - [ ] Subtotal calculates correctly
  - [ ] Discount applies correctly (promo codes)
  - [ ] Total calculates correctly
  - [ ] Shipping fee adds correctly

#### Payment Methods

##### KHQR Payment
- [ ] QR code generates correctly
- [ ] QR code displays in modal
- [ ] QR code expires after 10 minutes
- [ ] Payment polling checks status (every 1-1.5 seconds)
- [ ] Order created when payment confirmed
- [ ] Redirects to success page after payment
- [ ] Failed payment handled gracefully

##### ACLEDA Bank / Wing Money
- [ ] Payment method selection works
- [ ] QR code generates correctly
- [ ] Payment confirmation works
- [ ] Order created on confirmation

##### Cash on Delivery (COD)
- [ ] COD option available
- [ ] Order created immediately (no payment wait)
- [ ] Order status set to "pending"
- [ ] QR code generated for delivery confirmation
- [ ] Redirects to confirmation page
- [ ] Print receipt functionality works

#### Promo Codes
- [ ] **Valid Promo Code**
  - [ ] Accepts valid code
  - [ ] Calculates discount correctly (percentage)
  - [ ] Calculates discount correctly (fixed amount)
  - [ ] Respects minimum purchase requirement
  - [ ] Respects maximum discount limit
  - [ ] Updates total correctly
  - [ ] Success message displays

- [ ] **Invalid Promo Code**
  - [ ] Rejects expired code
  - [ ] Rejects code below minimum purchase
  - [ ] Rejects non-existent code
  - [ ] Rejects code that reached usage limit
  - [ ] Error message displays correctly

#### Order Creation
- [ ] **Order Processing**
  - [ ] Order number generated sequentially (MD00001, MD00002, etc.)
  - [ ] Order saved to database
  - [ ] Order items saved correctly
  - [ ] Customer created/updated correctly
  - [ ] Promo code usage tracked
  - [ ] Loyalty points calculated (if applicable)
  - [ ] Referral code processed (if applicable)
  - [ ] Order status set correctly based on payment method

---

### 📦 **Order Management**

#### Order Success Page
- [ ] Order number displays
- [ ] Order details correct
- [ ] Customer information correct
- [ ] Print receipt works
- [ ] Download receipt works
- [ ] Continue shopping button works

#### Order Tracking
- [ ] Track order by order number + phone
- [ ] Valid order displays correctly
- [ ] Invalid order number shows error
- [ ] Wrong phone number shows error
- [ ] Order status displays correctly
- [ ] Order items display correctly
- [ ] Order history shows for customer

---

### 👤 **User Registration & Login**

#### Customer Management
- [ ] Customer auto-created on first order
- [ ] Customer lookup by phone works
- [ ] Customer information updates on new order
- [ ] Referral code auto-generated (MD + last 6 digits)
- [ ] Loyalty points accumulate correctly

#### Password Reset (if applicable)
- [ ] Password reset email sends
- [ ] Reset link works
- [ ] New password saves correctly
- [ ] Old password invalid after reset

---

### 🔐 **Admin Panel**

#### Admin Access
- [ ] Admin login works
- [ ] Admin URL changeable (via ADMIN_URL env var)
- [ ] IP whitelist works (if enabled)
- [ ] Session expires correctly
- [ ] Logout works

#### Product Management
- [ ] Create product
- [ ] Edit product
- [ ] Delete product
- [ ] Upload product image
- [ ] Image validation works (size, format)
- [ ] Bulk import/export works
- [ ] Khmer text displays correctly in admin

#### Order Management
- [ ] View all orders
- [ ] Filter orders by status
- [ ] Filter orders by payment method
- [ ] Search orders by order number/phone
- [ ] View order details
- [ ] Update order status
- [ ] Cancel order
- [ ] Mark COD payment received
- [ ] Verify/reject orders
- [ ] Mark suspicious orders
- [ ] Sales report generates
- [ ] Commission report generates
- [ ] Export orders to Excel/CSV

#### Customer Management
- [ ] View all customers
- [ ] Search customers
- [ ] View customer orders
- [ ] View loyalty points
- [ ] View referral history

#### Promo Code Management
- [ ] Create promo code
- [ ] Edit promo code
- [ ] Deactivate promo code
- [ ] View usage statistics
- [ ] Bulk import/export promo codes

---

### 📝 **Form Validation**

#### Checkout Form
- [ ] Name: Required, max length
- [ ] Phone: Required, valid format
- [ ] Address: Required, max length
- [ ] Province: Required selection
- [ ] Email: Optional, valid format if provided

#### Admin Forms
- [ ] Product: All required fields validated
- [ ] Price: Must be positive number
- [ ] Stock: Must be non-negative integer
- [ ] Image: Valid format, size limit (5MB)
- [ ] Promo code: Unique code, valid dates
- [ ] Order: Status transitions validated

---

### 📱 **Mobile Responsiveness**

#### Mobile Devices (< 768px)
- [ ] Homepage layout responsive
- [ ] Product grid stacks correctly
- [ ] Navigation menu works (hamburger menu)
- [ ] Checkout form usable on mobile
- [ ] Payment modal displays correctly
- [ ] QR codes readable on mobile
- [ ] Forms easy to fill on mobile
- [ ] Buttons appropriately sized
- [ ] Text readable without zooming

#### Tablet Devices (768px - 1024px)
- [ ] Layout adapts correctly
- [ ] Product grid adjusts
- [ ] Forms usable
- [ ] Admin panel accessible

#### Desktop (> 1024px)
- [ ] Full layout displays correctly
- [ ] All features accessible
- [ ] No horizontal scrolling

---

### ⚡ **Performance Testing**

- [ ] **Page Load Times**
  - [ ] Homepage loads < 2 seconds
  - [ ] Checkout page loads < 2 seconds
  - [ ] Admin panel loads < 3 seconds
  - [ ] Product images load quickly
  - [ ] Static files served from CDN/WhiteNoise

- [ ] **Database Performance**
  - [ ] Product queries optimized
  - [ ] Order queries use indexes
  - [ ] No N+1 query problems
  - [ ] Database connection pooling works

- [ ] **Caching**
  - [ ] Product list cached (if enabled)
  - [ ] Static files cached
  - [ ] Session caching works (production)

---

### 🔒 **Security Testing**

#### CSRF Protection
- [ ] CSRF tokens required on forms
- [ ] CSRF tokens validated
- [ ] CSRF exempt endpoints documented
- [ ] API endpoints properly protected

#### SQL Injection
- [ ] All queries use Django ORM
- [ ] No raw SQL queries
- [ ] User input sanitized

#### XSS Protection
- [ ] User input escaped in templates
- [ ] JavaScript injection prevented
- [ ] CSP headers set correctly

#### File Upload Security
- [ ] Image uploads validated (format, size)
- [ ] File paths sanitized
- [ ] Uploaded files stored securely

#### Authentication & Authorization
- [ ] Admin requires authentication
- [ ] Session timeout works
- [ ] Passwords hashed (Django default)
- [ ] No sensitive data in URLs

#### Payment Security
- [ ] Payment data not logged
- [ ] Payment API calls secured
- [ ] QR codes expire after use
- [ ] Payment verification works

---

## 💳 Payment Processing Testing (Test Mode)

### Bakong API Testing

#### Test Credentials
- Use Bakong test/sandbox environment
- Test API keys (not production keys)
- Test merchant credentials

#### Test Scenarios

##### Successful Payment
1. Generate QR code
2. Scan QR code with test app
3. Complete test payment
4. Verify payment status changes to "confirmed"
5. Verify order status updates
6. Verify order created in database

##### Failed Payment
1. Generate QR code
2. Let QR code expire (wait 10+ minutes)
3. Verify QR code marked as expired
4. Verify order not created (or marked as failed)
5. Error message displays correctly

##### Payment Timeout
1. Generate QR code
2. Don't complete payment
3. Wait for timeout period
4. Verify polling stops
5. Verify appropriate error message

#### Testing Commands

```bash
# Test payment API endpoint (requires running server)
curl -X POST http://localhost:8000/api/payment/generate/ \
  -H "Content-Type: application/json" \
  -d '{"amount": 10.00, "order_id": "TEST001"}'

# Check payment status
curl "http://localhost:8000/api/payment/check/?md5=TEST_MD5"
```

---

## 👥 User Registration, Login, Password Reset Testing

### Customer Auto-Registration

- [ ] **First Order Creates Customer**
  - [ ] New phone number creates new customer
  - [ ] Customer ID generated (UUID)
  - [ ] Referral code auto-generated
  - [ ] Customer saved correctly

- [ ] **Returning Customer**
  - [ ] Existing phone number loads customer data
  - [ ] Customer information pre-fills form
  - [ ] Customer data updates if changed

### Admin Authentication

- [ ] **Login**
  - [ ] Valid credentials work
  - [ ] Invalid credentials rejected
  - [ ] Account lockout after failed attempts (if configured)

- [ ] **Session Management**
  - [ ] Session expires after 1 hour
  - [ ] Session refreshes on activity
  - [ ] Logout invalidates session

- [ ] **Password Reset** (if Django admin password reset enabled)
  - [ ] Password reset email sends
  - [ ] Reset link works
  - [ ] New password saves
  - [ ] Old password invalidated

---

## 🔧 Admin Panel Functionality Testing

### Product Management

- [ ] **CRUD Operations**
  - [ ] Create: All fields save correctly
  - [ ] Read: Product displays correctly
  - [ ] Update: Changes save correctly
  - [ ] Delete: Product removed (or soft-deleted)

- [ ] **Image Management**
  - [ ] Upload image works
  - [ ] Image preview displays
  - [ ] Image validation (size, format)
  - [ ] Image deletion works

- [ ] **Bulk Operations**
  - [ ] Import products from Excel/CSV
  - [ ] Export products to Excel/CSV
  - [ ] Khmer text imports/exports correctly

### Order Management

- [ ] **View Orders**
  - [ ] All orders display
  - [ ] Pagination works
  - [ ] Filters work (status, payment method, date)
  - [ ] Search works (order number, phone, name)

- [ ] **Order Actions**
  - [ ] Update order status
  - [ ] Cancel order
  - [ ] Mark COD payment received
  - [ ] Verify/reject order
  - [ ] Add notes
  - [ ] View order items

- [ ] **Reports**
  - [ ] Sales report generates
  - [ ] Date range filtering works
  - [ ] Commission report generates
  - [ ] Promoter statistics correct

### Promo Code Management

- [ ] **Create/Edit Promo Codes**
  - [ ] Code must be unique
  - [ ] Discount calculation works
  - [ ] Date range validation
  - [ ] Usage limit enforced

- [ ] **Promoter Management**
  - [ ] Assign promo code to promoter
  - [ ] Commission rate calculates correctly
  - [ ] Promoter statistics accurate

---

## ✅ Form Validation Testing

### Frontend Validation (JavaScript)

- [ ] **Checkout Form**
  - [ ] Required fields prevent submission
  - [ ] Phone format validated
  - [ ] Email format validated (if provided)
  - [ ] Real-time validation feedback

### Backend Validation (Django)

- [ ] **Order Creation**
  - [ ] Missing fields rejected (400 error)
  - [ ] Invalid data rejected
  - [ ] Empty cart rejected
  - [ ] Out-of-stock items rejected

- [ ] **Product Creation/Update**
  - [ ] Required fields validated
  - [ ] Price must be positive
  - [ ] Stock must be non-negative
  - [ ] Image format validated

- [ ] **Promo Code Validation**
  - [ ] Code format validated
  - [ ] Discount value validated
  - [ ] Date range validated
  - [ ] Minimum purchase validated

---

## 📱 Mobile Responsiveness Testing

### Test on Real Devices

#### iOS Devices
- [ ] iPhone SE (small screen)
- [ ] iPhone 12/13/14 (standard)
- [ ] iPhone 14 Pro Max (large)
- [ ] iPad (tablet)

#### Android Devices
- [ ] Small phone (< 5 inches)
- [ ] Standard phone (5-6 inches)
- [ ] Large phone (> 6 inches)
- [ ] Tablet

### Browser Testing

- [ ] Chrome (mobile)
- [ ] Safari (iOS)
- [ ] Firefox (mobile)
- [ ] Samsung Internet

### Responsive Breakpoints

- [ ] **Mobile (< 768px)**
  - [ ] Single column layout
  - [ ] Hamburger menu
  - [ ] Touch-friendly buttons
  - [ ] Forms stack vertically

- [ ] **Tablet (768px - 1024px)**
  - [ ] Two-column layout where appropriate
  - [ ] Navigation accessible
  - [ ] Forms usable

- [ ] **Desktop (> 1024px)**
  - [ ] Full layout
  - [ ] Multi-column grids
  - [ ] Hover effects work

---

## 🧪 Testing Tools & Commands

### Run Django Tests

```bash
# Run all tests
python manage.py test

# Run specific test class
python manage.py test app.tests.OrderFlowIntegrationTest

# Run with verbosity
python manage.py test --verbosity=2

# Run with coverage (if installed)
coverage run --source='.' manage.py test
coverage report
coverage html  # Open htmlcov/index.html in browser
```

### Manual Testing Checklist

1. **Start Server**
   ```bash
   python manage.py runserver
   ```

2. **Test Homepage**
   - Open http://127.0.0.1:8000/
   - Verify products display
   - Test add to cart

3. **Test Checkout**
   - Add items to cart
   - Go to checkout
   - Fill form
   - Test payment flow

4. **Test Admin**
   - Go to /admin/
   - Login
   - Test CRUD operations

5. **Test APIs**
   - Use Postman or curl
   - Test all endpoints
   - Verify responses

---

## 📊 Test Results Template

Use this template to document your test results:

```markdown
## Test Date: YYYY-MM-DD
## Tester: [Your Name]

### Product Features
- [x] Homepage loads - PASS
- [x] Add to cart - PASS
- [ ] Checkout - TODO

### Payment Testing
- [ ] KHQR payment - TODO
- [ ] COD payment - TODO

### Issues Found
1. [Issue description] - Status: Fixed/Pending
2. [Issue description] - Status: Pending
```

---

## 🚨 Common Issues & Solutions

### Issue: Tests failing due to missing dependencies
**Solution:** Install all requirements: `pip install -r requirements.txt`

### Issue: Payment API not working
**Solution:** 
1. Check Bakong API credentials in .env
2. Verify API endpoint is correct
3. Check network connectivity

### Issue: Static files not loading
**Solution:**
1. Run `python manage.py collectstatic`
2. Check STATIC_ROOT setting
3. Verify WhiteNoise middleware enabled

### Issue: Database errors
**Solution:**
1. Run migrations: `python manage.py migrate`
2. Check database connection settings
3. Verify PostgreSQL is running (if using)

---

## ✅ Sign-Off

**Testing Completed By:** _________________  
**Date:** _________________  
**Status:** ☐ Passed ☐ Failed (see issues above)  
**Ready for Production:** ☐ Yes ☐ No

---

**Next Steps:** If all tests pass, proceed to [PRODUCTION_DEPLOYMENT_CHECKLIST.md](./PRODUCTION_DEPLOYMENT_CHECKLIST.md)
