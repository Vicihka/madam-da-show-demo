# 📋 Full Workflow Explained - Step by Step

## 🎯 **Complete Order Journey**

This guide explains **exactly** what happens from when a customer orders to when delivery is complete.

---

## 👤 **PART 1: CUSTOMER ORDERS**

### **Step 1: Customer Browses Website**
- Customer visits: `http://127.0.0.1:8000/`
- Sees products on homepage
- Clicks "Add to Cart" for items they want

### **Step 2: Customer Goes to Checkout**
- Customer clicks cart icon
- Reviews items in cart
- Clicks "Checkout" button

### **Step 3: Customer Enters Information**
- Fills in form:
  - **Name** (e.g., "John Doe")
  - **Phone** (e.g., "012345678")
  - **Address** (e.g., "Street 123, Building 45")
  - **Province** (e.g., "Phnom Penh")
- Optionally enters **promo code** for discount
- Selects **payment method**:
  - **KHQR** (pay online now)
  - **Cash on Delivery** (pay when delivered)

### **Step 4: Payment Process**

#### **If Customer Chooses KHQR:**
1. Customer clicks "Pay with KHQR"
2. **QR code appears** on screen
3. Customer **scans QR code** with banking app (Bakong, ABA, ACLEDA, etc.)
4. Customer **pays in banking app**
5. System **checks payment** every few seconds
6. When payment confirmed → Order status: `confirmed`
7. Customer sees **success page**

#### **If Customer Chooses Cash on Delivery:**
1. Customer clicks "Cash on Delivery"
2. Order created **immediately** (no payment needed)
3. Order status: `pending`
4. Customer sees **success page** with order number
5. Customer will pay when order is delivered

### **Step 5: Order Created**
- **Order number generated** (e.g., MD00001)
- **Order saved to database**
- **Telegram notification sent** (if configured)
- **Order appears in employee dashboard** (within 3 seconds)

---

## 🔔 **PART 2: NOTIFICATIONS SENT**

### **What Happens When Order is Created:**

1. **Telegram Notification** (if configured)
   - Sent to admin/employee Telegram group
   - Shows order details:
     - Order number
     - Customer name & phone
     - Items ordered
     - Total amount
     - Payment method
   - Has **interactive buttons**:
     - "Start Preparing"
     - "View Details"
     - "Get QR Code Link" (for COD)

2. **Employee Dashboard Updates**
   - **Auto-refreshes every 3 seconds**
   - New order appears in "Orders to Prepare" section
   - **Alert banner** appears: "🔔 NEW ORDER RECEIVED!"
   - **Sound notification** plays (beep)
   - Order card has **red border** (new order highlight)

3. **Admin Panel**
   - Order visible in Django admin
   - Can view all order details
   - Can verify/manage order

---

## 👷 **PART 3: EMPLOYEE PREPARES ORDER**

### **Employee Has 2 Options:**

### **Option A: Employee Dashboard (Website)** ⭐ **RECOMMENDED**

**URL:** `http://127.0.0.1:8000/employee/`

#### **Step 1: Employee Sees New Order**
- Dashboard **auto-updates** every 3 seconds
- New order appears in **"Orders to Prepare"** section
- Employee sees:
  - Order number (e.g., MD00001)
  - Customer name & phone
  - **Product list** (what to prepare)
  - Total amount
  - Payment method

#### **Step 2: Employee Starts Preparing**
- Employee clicks **"👷 Start Preparing"** button
- Status changes to: `preparing`
- Order moves to **"Currently Preparing"** section
- Employee can see **product list** clearly:
  - Product 1 x 2
  - Product 2 x 1
  - etc.

#### **Step 3: Employee Prepares Products**
- Employee uses **product list** as guide
- Gathers all items
- Packs them in order package
- Checks everything is correct

#### **Step 4: Print QR Code (COD Orders Only)**
- If order is **Cash on Delivery**:
  - Employee clicks **"🖨️ Print QR Code"** button
  - Print page opens in new tab
  - Employee prints QR code
  - **Attaches QR code** to order package
  - QR code will be used by driver to confirm payment

#### **Step 5: Mark as Ready**
- After preparing everything:
  - Employee clicks **"✅ Mark Ready"** button
  - Status changes to: `ready_for_delivery`
  - Order moves to **"Ready for Delivery"** section
  - Order is ready for driver pickup

---

### **Option B: Telegram Bot** (Alternative)

**No website needed - everything in Telegram!**

#### **Step 1: Employee Receives Notification**
- Gets Telegram message with order details
- Sees **interactive buttons**

#### **Step 2: Employee Clicks Buttons**
- Clicks **"👷 Start Preparing"** → Status updates
- Clicks **"🖨️ Get QR Code Link"** (COD) → Gets print link
- Clicks **"📦 Mark Ready"** → Status updates
- All updates happen **instantly** in Telegram

#### **Step 3: Employee Uses Commands**
- `/orders` - View pending orders
- `/preparing` - View orders being prepared
- `/order MD00001` - View specific order

---

## 🚚 **PART 4: DELIVERY PROCESS**

### **Step 1: Driver Picks Up Order**
- Driver arrives at warehouse
- Employee gives driver the order package
- Employee clicks **"🚚 Out for Delivery"** button
- Status changes to: `out_for_delivery`
- Order moves to **"Out for Delivery"** section

### **Step 2: Driver Delivers to Customer**
- Driver goes to customer address
- Delivers products to customer
- Customer receives order

### **Step 3: Payment Collection (COD Only)**

#### **If Cash on Delivery:**
1. Driver collects payment from customer
2. Driver confirms payment using **one of these methods:**

   **Method A: Scan QR Code** (Easiest)
   - Driver scans QR code with phone camera
   - Confirmation page opens automatically
   - Driver clicks **"Confirm Payment"**
   - Payment confirmed instantly!

   **Method B: Enter Order Number**
   - Driver goes to: `http://127.0.0.1:8000/cod/confirm/`
   - Enters order number (e.g., MD00001)
   - Clicks **"Confirm Payment"**
   - Payment confirmed!

   **Method C: API** (For mobile apps)
   - Mobile app calls API
   - Sends order number
   - Payment confirmed programmatically

3. **Payment Confirmed:**
   - Order status: `confirmed`
   - `payment_received` = True
   - `payment_received_at` = Current time
   - Telegram notification sent (if configured)
   - Order complete!

#### **If KHQR Payment:**
- Payment already received online
- No need to collect payment
- Order already confirmed

### **Step 4: Mark as Delivered**
- After delivery complete:
  - Employee clicks **"✅ Delivered"** button (or driver confirms)
  - Status changes to: `delivered`
  - Order complete! ✅

---

## 👨‍💼 **PART 5: ADMIN MANAGEMENT**

### **Admin Controls Everything:**

**URL:** `http://127.0.0.1:8000/admin/`

#### **What Admin Can Do:**

1. **View All Orders**
   - See all orders in one place
   - Filter by status, payment method, date
   - Search by order number, customer name

2. **Verify Orders**
   - Check for suspicious orders
   - Verify customer information
   - Mark as verified/rejected

3. **View Reports**
   - **Sales Report**: Total revenue, orders count
   - **Commission Report**: Promoter commissions
   - Filter by date range

4. **Manage COD Orders**
   - See payment status
   - Manually confirm payment (if needed)
   - Print QR codes
   - View delivery notes

5. **Manage Products**
   - Add/edit products
   - Update prices
   - Manage inventory

---

## 📊 **PART 6: ORDER STATUS FLOW**

### **Complete Status Journey:**

```
1. Customer Orders
   ↓
   Status: pending (COD) or confirmed (KHQR)
   ↓
   [Employee: Start Preparing]
   ↓
2. Status: preparing
   ↓
   [Employee: Print QR Code] (COD only)
   ↓
   [Employee: Mark Ready]
   ↓
3. Status: ready_for_delivery
   ↓
   [Employee: Out for Delivery]
   ↓
4. Status: out_for_delivery
   ↓
   [Driver: Deliver & Confirm Payment] (COD)
   OR
   [Employee: Mark Delivered]
   ↓
5. Status: delivered ✅
```

### **Status Meanings:**

- **pending** - New COD order, waiting for preparation
- **confirmed** - Payment received (KHQR) or verified
- **preparing** - Employee is preparing the order
- **ready_for_delivery** - Order ready for driver pickup
- **out_for_delivery** - Driver has order, delivering
- **delivered** - Order delivered and complete
- **cancelled** - Order cancelled

---

## ⏱️ **PART 7: TIMELINE EXAMPLE**

### **Real-World Example:**

**Day 1 - Morning:**

- **10:00 AM** - Customer browses website
- **10:05 AM** - Customer adds products to cart
- **10:10 AM** - Customer checks out, selects COD
- **10:11 AM** - Order created (MD00001)
  - Status: `pending`
  - Telegram notification sent
  - Appears in employee dashboard

**Day 1 - Employee Prepares:**

- **10:15 AM** - Employee sees notification (Telegram or dashboard)
- **10:16 AM** - Employee clicks "Start Preparing"
  - Status: `preparing`
- **10:20 AM** - Employee prepares products
  - Uses product list as guide
- **10:25 AM** - Employee prints QR code (COD order)
- **10:30 AM** - Employee clicks "Mark Ready"
  - Status: `ready_for_delivery`

**Day 1 - Driver Picks Up:**

- **11:00 AM** - Driver arrives at warehouse
- **11:05 AM** - Employee clicks "Out for Delivery"
  - Status: `out_for_delivery`
- **11:10 AM** - Driver leaves with order

**Day 1 - Delivery:**

- **2:00 PM** - Driver arrives at customer address
- **2:05 PM** - Driver delivers products
- **2:06 PM** - Customer pays $50 cash
- **2:07 PM** - Driver scans QR code
- **2:08 PM** - Driver clicks "Confirm Payment"
  - Status: `confirmed`
  - `payment_received` = True
  - Telegram notification sent
- **2:10 PM** - Order complete! ✅

---

## 🔄 **PART 8: REAL-TIME UPDATES**

### **How Everything Stays Updated:**

1. **Employee Dashboard**
   - **Auto-refreshes every 3 seconds**
   - New orders appear automatically
   - Status updates instantly
   - No page reload needed

2. **Telegram Bot**
   - **Instant notifications** when orders created
   - **Button clicks** update status immediately
   - **Commands** show latest orders

3. **Admin Panel**
   - Always shows current data
   - Refresh to see latest updates

---

## 🎯 **PART 9: KEY FEATURES**

### **For Customers:**
- ✅ Easy ordering process
- ✅ Multiple payment options
- ✅ Order confirmation
- ✅ Track order status

### **For Employees:**
- ✅ **Real-time dashboard** - see orders instantly
- ✅ **Product lists** - know what to prepare
- ✅ **Quick actions** - one-click status updates
- ✅ **QR code printing** - easy for COD
- ✅ **Telegram integration** - manage from phone
- ✅ **Sound notifications** - never miss an order

### **For Drivers:**
- ✅ **QR code scanning** - easy payment confirmation
- ✅ **Mobile-friendly** - works on phones
- ✅ **Simple process** - scan and confirm

### **For Admin:**
- ✅ **Full control** - manage everything
- ✅ **Reports** - track sales and commissions
- ✅ **Verification** - check suspicious orders
- ✅ **Analytics** - see business performance

---

## 📱 **PART 10: ACCESS POINTS**

### **Customer:**
- **Shop:** `http://127.0.0.1:8000/`
- **Checkout:** `http://127.0.0.1:8000/checkout/`

### **Employee:**
- **Dashboard:** `http://127.0.0.1:8000/employee/`
- **Telegram:** Use bot commands

### **Driver:**
- **COD Confirm:** `http://127.0.0.1:8000/cod/confirm/`

### **Admin:**
- **Admin Panel:** `http://127.0.0.1:8000/admin/`

---

## ✅ **PART 11: SUMMARY**

### **Complete Flow:**

```
Customer Orders
    ↓
Notification Sent (Telegram + Dashboard)
    ↓
Employee Sees Order (Real-time)
    ↓
Employee Starts Preparing
    ↓
Employee Prepares Products (Uses Product List)
    ↓
Employee Prints QR Code (COD)
    ↓
Employee Marks Ready
    ↓
Driver Picks Up
    ↓
Driver Delivers
    ↓
Driver Confirms Payment (COD - Scan QR)
    ↓
Order Complete ✅
```

### **Key Points:**

1. **Everything is Real-Time**
   - Orders appear instantly
   - Updates happen immediately
   - No delays

2. **Easy for Everyone**
   - Customers: Simple ordering
   - Employees: Clear workflow
   - Drivers: Easy confirmation
   - Admin: Full control

3. **Multiple Options**
   - Website dashboard
   - Telegram bot
   - Mobile-friendly
   - Works everywhere

4. **Professional System**
   - Automated notifications
   - Real-time updates
   - Clear status tracking
   - Complete workflow

---

## 🎉 **Your Complete Workflow is Ready!**

**Everything works together:**
- ✅ Customer orders → Employee sees → Prepares → Driver delivers → Payment confirmed → Complete!

**All systems connected:**
- ✅ Website → Dashboard → Telegram → Admin → Everything!

**Fast and efficient:**
- ✅ Real-time updates → Quick actions → Instant notifications → Professional workflow!

**Your business is fully automated and ready to scale!** 🚀

