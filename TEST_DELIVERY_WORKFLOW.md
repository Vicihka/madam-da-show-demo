# 🚚 Testing Delivery Workflow

## Complete Order Status Flow

The delivery workflow has 5 main stages:

1. **Pending/Confirmed** → New orders waiting to be prepared
2. **Preparing** → Orders being prepared by employees
3. **Ready for Delivery** → Orders ready to be picked up by delivery driver
4. **Out for Delivery** → Orders currently being delivered
5. **Delivered** → Orders successfully delivered (removed from dashboard)

---

## Step-by-Step Test Instructions

### Step 1: Create a Test Order

1. Go to your shop: `http://127.0.0.1:8000/`
2. Add products to cart
3. Go to checkout
4. Fill in customer details
5. Choose payment method (KHQR or Cash on Delivery)
6. Complete the order

**Expected Result:**
- Order appears in "📋 Orders to Prepare" section
- Status shows as "Pending" or "Confirmed"

---

### Step 2: Start Preparing

1. Open Employee Dashboard: `http://127.0.0.1:8000/employee/`
2. Find your test order in "📋 Orders to Prepare"
3. Click **"👷 Start Preparing"** button

**Expected Result:**
- Order moves to "⚙️ Currently Preparing" section
- Status changes to "Preparing"
- Button changes to "✅ Mark Ready"

---

### Step 3: Mark Ready for Delivery

1. In "⚙️ Currently Preparing" section
2. Click **"✅ Mark Ready"** button

**Expected Result:**
- Order moves to "✅ Ready for Delivery" section
- Status changes to "Ready for Delivery"
- Button changes to "🚚 Out for Delivery"

---

### Step 4: Out for Delivery

1. In "✅ Ready for Delivery" section
2. Click **"🚚 Out for Delivery"** button

**Expected Result:**
- Order moves to "🚚 Out for Delivery" section
- Status changes to "Out for Delivery"
- Button changes to "✅ Delivered"

---

### Step 5: Mark as Delivered

1. In "🚚 Out for Delivery" section
2. Click **"✅ Delivered"** button

**Expected Result:**
- Order disappears from dashboard (delivered orders are hidden)
- Status changes to "Delivered" in database
- Order is complete!

---

## Quick Test Checklist

- [ ] Order appears in "To Prepare" after creation
- [ ] Order moves to "Preparing" when "Start Preparing" clicked
- [ ] Order moves to "Ready for Delivery" when "Mark Ready" clicked
- [ ] Order moves to "Out for Delivery" when "Out for Delivery" clicked
- [ ] Order disappears when "Delivered" clicked
- [ ] Counters update correctly in each section
- [ ] WebSocket updates work (no page refresh needed)
- [ ] Status updates happen immediately (no confirmation dialog)

---

## Testing COD (Cash on Delivery) Orders

For COD orders, you can also test:

1. **Print QR Code** - Click "🖨️ Print QR" button when order is "Preparing"
   - Should open a printable page with QR code
   - QR code can be scanned to confirm payment

2. **Confirm Payment** - After delivery, driver can scan QR code
   - Visit: `http://127.0.0.1:8000/cod/confirm/{ORDER_NUMBER}/`
   - Enter order number and confirm payment

---

## Testing Multiple Orders

To test with multiple orders:

1. Create 3-5 test orders
2. Process them through the workflow:
   - Start preparing all
   - Mark ready one by one
   - Send out for delivery
   - Mark as delivered

**Expected Result:**
- All orders move smoothly between sections
- Counters update correctly
- No duplicate orders
- Real-time updates work

---

## Troubleshooting

**If orders don't move:**
- Check browser console (F12) for errors
- Verify WebSocket is connected (should show "🟢 Real-time: ON")
- Try refreshing the page

**If status doesn't update:**
- Check server logs for errors
- Verify Redis is running
- Check database connection

---

## Quick Test Commands

You can also test via Django shell:

```python
python manage.py shell

from app.models import Order
order = Order.objects.first()
print(f"Order: {order.order_number}, Status: {order.status}")

# Change status
order.status = 'preparing'
order.save()
print(f"Updated to: {order.status}")
```

---

## Expected Dashboard Sections

1. **📋 Orders to Prepare** - New orders (Pending/Confirmed)
2. **⚙️ Currently Preparing** - Orders being prepared
3. **✅ Ready for Delivery** - Orders ready to go
4. **🚚 Out for Delivery** - Orders being delivered
5. **Delivered orders** - Hidden from dashboard (completed)

---

Happy Testing! 🎉

