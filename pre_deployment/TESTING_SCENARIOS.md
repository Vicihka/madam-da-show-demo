# 🧪 Comprehensive Testing Scenarios - MADAM DA E-Commerce

This document provides detailed test cases for all critical e-commerce flows.

---

## 📦 Scenario 1: Complete Purchase Flow

### Test Case: Successful Purchase with KHQR Payment

**Preconditions:**
- Products exist in database
- Bakong API credentials configured
- Server running

**Test Steps:**
1. **Add Product to Cart**
   - Navigate to homepage
   - Click "Add to Cart" on a product
   - Verify cart count badge updates
   - Verify product appears in cart

2. **Navigate to Checkout**
   - Click cart icon or checkout button
   - Verify checkout page loads
   - Verify cart items display correctly
   - Verify subtotal calculates correctly

3. **Fill Checkout Form**
   - Enter name: "Test Customer"
   - Enter phone: "012345678"
   - Enter address: "123 Test Street"
   - Select province: "Phnom Penh"
   - Verify form accepts input

4. **Select Payment Method**
   - Select "KHQR" payment method
   - Verify payment method selected

5. **Submit Order**
   - Click "Place Order" or submit form
   - Verify payment modal opens
   - Verify QR code generates and displays
   - Verify order number shown (or "Processing...")

6. **Complete Payment (Simulate)**
   - Scan QR code with Bakong app (test mode)
   - Complete payment
   - Wait for payment confirmation (polling)

7. **Verify Order Created**
   - Verify redirect to success page
   - Verify order number displays
   - Check admin panel: order exists
   - Verify order status is "confirmed"
   - Verify order items saved correctly

**Expected Results:**
- ✅ Order created with sequential number (MD00001, MD00002, etc.)
- ✅ Customer created/updated
- ✅ Order items saved correctly
- ✅ Payment status confirmed
- ✅ Success page displays correctly

**Post-Conditions:**
- Order exists in database
- Customer exists in database
- Order status: "confirmed"

---

## 💳 Scenario 2: Failed Payment Handling

### Test Case: Payment Timeout / Failed Payment

**Preconditions:**
- Checkout form filled
- Payment method selected (KHQR)

**Test Steps:**
1. Generate QR code
2. **Don't complete payment**
3. Wait for QR code expiration (10+ minutes)
4. Verify payment polling stops
5. Verify appropriate error message displays
6. Verify user can retry payment

**Expected Results:**
- ✅ QR code expires after 10 minutes
- ✅ Error message: "Payment timeout" or similar
- ✅ Order NOT created (or created with "failed" status)
- ✅ User can retry payment or cancel

**Alternative Test: Simulate Payment Failure**
1. Generate QR code
2. Simulate payment failure (if Bakong API supports this)
3. Verify error handling
4. Verify order status

---

## 📦 Scenario 3: Out of Stock Products

### Test Case: Attempt to Order Out of Stock Product

**Preconditions:**
- Product exists with stock = 0

**Test Steps:**
1. Navigate to product (if visible)
2. Attempt to add to cart
3. Verify product cannot be added (or shows out of stock)
4. If product already in cart:
   - Attempt to checkout
   - Verify validation prevents checkout
   - Verify error message: "Product out of stock"

**Expected Results:**
- ✅ Out of stock products cannot be added to cart
- ✅ Out of stock products show "Out of Stock" badge
- ✅ Checkout blocked if cart contains out of stock items
- ✅ Error message displayed

---

## 🎟️ Scenario 4: Invalid Coupon Codes

### Test Case: Apply Invalid Promo Code

**Test Steps:**
1. Add products to cart
2. Go to checkout
3. Enter invalid promo code (e.g., "INVALID123")
4. Click "Apply"
5. Verify error message displays

**Sub-scenarios:**

#### 4a. Expired Promo Code
- Create promo code with past expiry date
- Attempt to use it
- Verify error: "Promo code has expired"

#### 4b. Code Below Minimum Purchase
- Create promo code with min_purchase = $50
- Cart total = $30
- Attempt to use code
- Verify error: "Minimum order amount is $50"

#### 4c. Code Reached Usage Limit
- Create promo code with usage_limit = 1
- Use code once (create order)
- Attempt to use again
- Verify error: "Promo code has reached usage limit"

**Expected Results:**
- ✅ Invalid codes rejected
- ✅ Appropriate error messages shown
- ✅ Valid codes work correctly
- ✅ Discount calculates correctly

---

## 👨‍💼 Scenario 5: Admin Order Management

### Test Case: Admin Updates Order Status

**Preconditions:**
- Admin user logged in
- Order exists in system

**Test Steps:**
1. **Login to Admin Panel**
   - Navigate to /admin/
   - Login with admin credentials
   - Verify dashboard loads

2. **View Orders**
   - Navigate to Orders section
   - Verify orders list displays
   - Verify filters work (status, payment method, date)

3. **Update Order Status**
   - Click on an order
   - Change status from "pending" to "confirmed"
   - Save
   - Verify status updated

4. **Verify Status Transitions**
   - Test valid transitions:
     - pending → confirmed ✓
     - confirmed → preparing ✓
     - preparing → ready_for_delivery ✓
   - Test invalid transitions:
     - delivered → pending ✗ (should fail or prevent)

5. **Mark COD Payment Received**
   - Find COD order
   - Use admin action "Confirm COD Payment Received"
   - Verify payment_received = True
   - Verify status changes to "confirmed"

**Expected Results:**
- ✅ Order status updates correctly
- ✅ Valid transitions allowed
- ✅ Invalid transitions prevented
- ✅ COD payment marking works
- ✅ WebSocket notification sent (if enabled)

---

## 🔄 Scenario 6: Browser Closed During Checkout

### Test Case: User Closes Browser During Payment

**Preconditions:**
- User on checkout page
- QR code generated

**Test Steps:**
1. Fill checkout form
2. Submit order
3. QR code displays
4. **Close browser tab/window**
5. Complete payment (if possible) OR
6. Reopen browser, go to track order page
7. Enter order number and phone
8. Verify order status

**Expected Results:**
- ✅ Order created before payment confirmation (if applicable)
- ✅ Order can be tracked
- ✅ Payment can complete if QR code still valid
- ✅ Order status updates when payment confirms

**Important Considerations:**
- QR codes expire after 10 minutes
- Payment polling happens on frontend (stops if browser closed)
- Backend should handle payment confirmation independently

---

## 👥 Scenario 7: Concurrent Users Ordering Same Product

### Test Case: Multiple Users Order Last Item in Stock

**Preconditions:**
- Product with stock = 1

**Test Steps:**
1. **User 1:**
   - Add product to cart
   - Fill checkout form
   - Submit order

2. **User 2: (Simultaneously)**
   - Add same product to cart
   - Fill checkout form
   - Submit order

3. **Verify Results:**
   - Check which order succeeded
   - Check which order failed (out of stock)
   - Verify stock reduced correctly
   - Verify error message for failed order

**Expected Results:**
- ✅ Only one order succeeds
- ✅ Second order fails with "Out of stock" error
- ✅ Stock = 0 after successful order
- ✅ Database integrity maintained (no race conditions)

**Technical Note:**
- Use database transactions with SELECT FOR UPDATE
- Or use atomic operations for stock decrement
- Consider optimistic locking

---

## 🛒 Scenario 8: Cart Persistence

### Test Case: Cart Persists Across Sessions

**Test Steps:**
1. Add products to cart
2. **Close browser**
3. **Reopen browser**
4. Navigate to site
5. Verify cart items still present
6. Verify cart count correct

**Expected Results:**
- ✅ Cart stored in localStorage
- ✅ Cart persists across browser sessions
- ✅ Cart persists across page reloads
- ✅ Cart clears after successful order

---

## 📱 Scenario 9: Mobile Checkout Flow

### Test Case: Complete Purchase on Mobile Device

**Test Steps:**
1. Open site on mobile browser
2. Navigate to homepage
3. Add product to cart (tap)
4. Go to checkout
5. Fill form using mobile keyboard
6. Select payment method
7. Generate QR code
8. Scan QR code with mobile payment app
9. Complete payment
10. Verify success page displays correctly

**Expected Results:**
- ✅ Mobile layout renders correctly
- ✅ Forms usable on mobile
- ✅ Buttons appropriately sized
- ✅ QR code scannable from mobile screen
- ✅ Payment flow works on mobile

---

## 🔄 Scenario 10: Order Status Updates (WebSocket)

### Test Case: Real-time Order Status Updates

**Preconditions:**
- Employee dashboard open
- WebSocket connection established

**Test Steps:**
1. Customer places order
2. Verify order appears on employee dashboard immediately
3. Admin updates order status
4. Verify status updates on dashboard in real-time
5. Test multiple status updates

**Expected Results:**
- ✅ New orders appear immediately
- ✅ Status updates broadcast in real-time
- ✅ WebSocket connection stable
- ✅ Handles disconnection/reconnection

---

## 💰 Scenario 11: Promo Code with Multiple Conditions

### Test Case: Complex Promo Code Validation

**Preconditions:**
- Promo code: 20% off, min $50, max discount $20, usage limit 100

**Test Steps:**
1. Cart total: $30 (below minimum)
   - Apply code → Should fail: "Minimum order amount is $50"

2. Cart total: $50 (at minimum)
   - Apply code → Should work: $10 discount (20% of $50)

3. Cart total: $200 (exceeds max discount)
   - Apply code → Should work: $20 discount (capped at max)

4. Use code 100 times (reach usage limit)
   - Apply code → Should fail: "Promo code has reached usage limit"

**Expected Results:**
- ✅ All conditions validated correctly
- ✅ Discount calculates correctly
- ✅ Usage limit enforced

---

## 🔐 Scenario 12: Security Testing

### Test Case: SQL Injection Attempt

**Test Steps:**
1. In checkout form, enter SQL injection in name field:
   ```
   Test'; DROP TABLE orders; --
   ```
2. Submit form
3. Verify order created safely
4. Verify database not affected

**Expected Results:**
- ✅ Input sanitized (escaped)
- ✅ Database safe
- ✅ No SQL executed

### Test Case: XSS Attempt

**Test Steps:**
1. Enter XSS payload in form:
   ```html
   <script>alert('XSS')</script>
   ```
2. Submit form
3. View order in admin panel
4. Verify script not executed
5. Verify input escaped/displayed as text

**Expected Results:**
- ✅ XSS prevented
- ✅ Input escaped in templates
- ✅ Script tags displayed as text

---

## 📊 Test Results Template

```markdown
## Test Execution Log

**Date:** 2024-01-15
**Tester:** [Name]
**Environment:** Development/Staging/Production

### Scenario 1: Complete Purchase Flow
- [ ] All steps completed
- [ ] Results match expected
- [ ] Issues found: [None/List issues]

### Scenario 2: Failed Payment
- [ ] Tested
- [ ] Results: [Pass/Fail]
- [ ] Notes: [Any observations]

[... continue for all scenarios ...]

### Summary
- Total Scenarios: X
- Passed: Y
- Failed: Z
- Blocked: A

### Critical Issues Found
1. [Issue description]
   - Severity: Critical/High/Medium/Low
   - Status: Open/Fixed/Deferred

2. [Issue description]
   ...
```

---

## 🚨 Edge Cases to Test

### Order Number Generation
- [ ] First order generates MD00001
- [ ] Subsequent orders increment correctly
- [ ] Handles deleted orders correctly
- [ ] No duplicate order numbers

### Customer Creation
- [ ] New phone creates new customer
- [ ] Existing phone updates customer info
- [ ] Referral code auto-generated correctly
- [ ] Customer ID is UUID

### Payment Edge Cases
- [ ] Payment completes after QR expiration (should fail)
- [ ] Multiple payment attempts for same order
- [ ] Payment amount mismatch
- [ ] Network failure during payment

### Stock Management
- [ ] Stock decrements on order creation
- [ ] Stock doesn't go negative
- [ ] Concurrent orders handled correctly
- [ ] Stock updates reflect immediately

---

## ✅ Sign-Off

**All scenarios tested:** ☐ Yes ☐ No  
**Critical issues resolved:** ☐ Yes ☐ No  
**Ready for production:** ☐ Yes ☐ No

**Tester Signature:** _________________  
**Date:** _________________
