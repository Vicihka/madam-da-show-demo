# 📝 Checkout Page: Delivery Note & Telegram Toggle Explanation

## Overview

This document explains how the **Delivery Note** and **Telegram Contact Toggle** work in the checkout page (`templates/app/checkout.html`).

---

## 🔍 Current Status

### ❌ **IMPORTANT: These Features Are NOT Currently Working**

Both the delivery note and Telegram toggle exist in the HTML, but **they are not being collected or sent to the backend**. Here's what's happening:

---

## 📋 1. Delivery Note (`delivery-note`)

### **HTML Element:**
```html
<textarea class="form-textarea" id="delivery-note" name="deliveryNote" rows="3" 
          autocomplete="off" placeholder="Optional delivery notes"></textarea>
```

### **Current Behavior:**
- ✅ Field exists in the form
- ✅ User can type in it
- ❌ **Value is NOT collected in JavaScript**
- ❌ **Value is NOT sent to backend API**
- ❌ **Value is NOT saved to database**

### **Where It SHOULD Go:**
The `Order` model has a `notes` field (line 143 in `app/models.py`):
```python
notes = models.TextField(blank=True, null=True)
```

This field can store delivery notes, but currently it's never being populated from the checkout form.

---

## 📱 2. Telegram Toggle (`telegram-toggle`)

### **HTML Element:**
```html
<button type="button" class="toggle-switch" id="telegram-toggle" 
        data-state="unchecked" onclick="toggleTelegram(this)">
    <span class="toggle-thumb"></span>
</button>
<label class="toggle-label">Contact via Telegram</label>
```

### **Current Behavior:**
- ✅ Toggle button exists and works (can be clicked)
- ✅ Visual state changes (checked/unchecked)
- ✅ JavaScript function `toggleTelegram()` works
- ❌ **State is NOT checked when creating order**
- ❌ **Telegram notifications are ALWAYS sent** (regardless of toggle state)

### **Where Telegram Notifications Go:**
Telegram notifications are sent to:
- **Admin Telegram Chat** (configured in `settings.TELEGRAM_CHAT_ID`)
- Sent via `send_telegram_notification()` function in `app/views.py`
- Triggered automatically when order is created (lines 1150-1153 in `views.py`)

**Currently:** All orders trigger Telegram notifications regardless of the toggle state.

---

## 🔧 How to Fix (If You Want These Features to Work)

### **Fix 1: Make Delivery Note Work**

**Step 1: Collect the value in JavaScript**

In `static/js/checkout.js`, find `createOrderForCOD()` function (around line 630) and `createOrderOnPaymentConfirmation()` function (around line 867):

**Current code:**
```javascript
const orderData = {
    name: name,
    phone: phone,
    address: address,
    province: province,
    payment_method: paymentMethodName,
    total: total.toFixed(2),
    subtotal: subtotal.toFixed(2),
    discount: discountAmount.toFixed(2),
    items: cart
};
```

**Add delivery note:**
```javascript
// Get delivery note
const deliveryNote = document.getElementById('delivery-note')?.value || '';

const orderData = {
    name: name,
    phone: phone,
    address: address,
    province: province,
    delivery_note: deliveryNote,  // ADD THIS LINE
    payment_method: paymentMethodName,
    total: total.toFixed(2),
    subtotal: subtotal.toFixed(2),
    discount: discountAmount.toFixed(2),
    items: cart
};
```

**Step 2: Save to database in backend**

In `app/views.py`, `create_order_on_payment()` function (around line 894):

**Current code:**
```python
data = json.loads(request.body)
name = data.get('name', '').strip()
phone = data.get('phone', '').strip()
address = data.get('address', '').strip()
province = data.get('province', '').strip()
```

**Add:**
```python
delivery_note = data.get('delivery_note', '').strip()
```

Then when creating the order (around line 983):
```python
order = Order(
    customer=customer,
    customer_name=name,
    customer_phone=phone,
    customer_address=address,
    customer_province=province,
    notes=delivery_note,  # ADD THIS LINE - saves to Order.notes field
    subtotal=subtotal,
    shipping_fee=Decimal('0.00'),
    discount_amount=discount_amount,
    total=total,
    payment_method=payment_method,
    status=order_status,
    customer_received=False,
    payment_received=False
)
```

---

### **Fix 2: Make Telegram Toggle Work**

**Step 1: Check toggle state in JavaScript**

In `static/js/checkout.js`, in both `createOrderForCOD()` and `createOrderOnPaymentConfirmation()`:

**Add:**
```javascript
// Check if Telegram notification is enabled
const telegramToggle = document.getElementById('telegram-toggle');
const notifyViaTelegram = telegramToggle?.getAttribute('data-state') === 'checked';

const orderData = {
    // ... other fields ...
    notify_via_telegram: notifyViaTelegram,  // ADD THIS LINE
};
```

**Step 2: Check value in backend**

In `app/views.py`, `create_order_on_payment()` function:

**Add:**
```python
notify_via_telegram = data.get('notify_via_telegram', True)  # Default to True for backward compatibility
```

**Step 3: Conditionally send Telegram notification**

Replace the automatic notification (around line 1150):

**Current code:**
```python
# Send Telegram notification immediately when payment is confirmed
order.refresh_from_db()
try:
    logger.info(f"Payment confirmed - Order created: {order.order_number}, sending Telegram notification...")
    send_telegram_notification(order)
except Exception as e:
    logger.error(f"Failed to send Telegram notification: {str(e)}", exc_info=True)
```

**Change to:**
```python
# Send Telegram notification only if customer opted in
order.refresh_from_db()
if notify_via_telegram:
    try:
        logger.info(f"Payment confirmed - Order created: {order.order_number}, sending Telegram notification...")
        send_telegram_notification(order)
    except Exception as e:
        logger.error(f"Failed to send Telegram notification: {str(e)}", exc_info=True)
else:
    logger.info(f"Order {order.order_number} created - Telegram notification skipped (customer opted out)")
```

---

## 📊 Summary: Current Data Flow

### **Delivery Note:**
```
User types in textarea
    ↓
[NOT COLLECTED] ❌
    ↓
[NOT SENT TO API] ❌
    ↓
[NOT SAVED TO DATABASE] ❌
```

### **Telegram Toggle:**
```
User clicks toggle (checked/unchecked)
    ↓
Toggle state changes visually ✅
    ↓
[NOT CHECKED WHEN ORDER CREATED] ❌
    ↓
Telegram notification ALWAYS sent regardless ❌
```

---

## 🎯 Where Telegram Notifications Currently Go

When an order is created, a Telegram notification is automatically sent to:

1. **Admin Telegram Chat ID** (configured in Django settings)
   - Set in `settings.TELEGRAM_CHAT_ID`
   - This is where all order notifications go

2. **Message Content:**
   - Order number
   - Customer name and phone
   - Total amount
   - Payment method
   - Order items

3. **When It's Sent:**
   - Immediately when order is created
   - For both COD and KHQR payments
   - Always sent (currently ignores toggle state)

**Example Telegram Message:**
```
🛒 NEW ORDER RECEIVED!

📦 Order: MD001234
👤 Customer: John Doe
📱 Phone: +855123456789
💵 Total: $49.99
💳 Payment: Cash on Delivery

[Order Items List]
```

---

## 💡 Recommendation

### **Option 1: Remove Unused Features**
If the client doesn't need these features:
- Remove the delivery note textarea
- Remove the Telegram toggle
- Keep Telegram notifications always on (current behavior)

### **Option 2: Implement the Features**
If the client wants these features:
- Implement the fixes above
- Test thoroughly
- Update documentation

### **Option 3: Keep as Placeholder**
Leave as-is if you plan to implement later, but make it clear to client that these features don't work yet.

---

## 🔍 Testing Checklist

If you implement the fixes:

### **Delivery Note:**
- [ ] Type note in checkout
- [ ] Complete order
- [ ] Check admin panel → Orders → Open order
- [ ] Verify note appears in `notes` field

### **Telegram Toggle:**
- [ ] Toggle OFF → Create order → Verify NO Telegram message
- [ ] Toggle ON → Create order → Verify Telegram message received
- [ ] Test with both COD and KHQR payments

---

## 📝 Database Field Reference

### **Order Model Fields (relevant):**

1. **`notes`** (TextField, optional)
   - Currently: Not used
   - Purpose: Store delivery notes from customer
   - Should be: Populated from `delivery-note` textarea

2. **`cod_delivery_notes`** (TextField, optional)
   - Currently: Used for driver/admin notes when confirming COD payment
   - Purpose: Notes about delivery/payment collection
   - Different from: Customer delivery notes

---

## 🚀 Quick Implementation Summary

**To make delivery note work:**
1. Collect value from `#delivery-note` in JavaScript
2. Send as `delivery_note` in API request
3. Save to `Order.notes` field in backend

**To make Telegram toggle work:**
1. Check `telegram-toggle` data-state in JavaScript
2. Send as `notify_via_telegram` boolean in API request
3. Conditionally call `send_telegram_notification()` based on value

---

**Last Updated:** 2025-12-16  
**Status:** Features exist but not functional - needs implementation
