# 🤖 Telegram Bot Setup for Employees

## ✅ **What You Can Do with Telegram Bot**

Your employees can now manage orders **directly from Telegram** - no need to open the website!

### **Features:**
- ✅ **Instant notifications** when new orders come in
- ✅ **View orders** by status (pending, preparing, ready, etc.)
- ✅ **Update order status** with one click
- ✅ **Get QR code links** for COD orders
- ✅ **View order details** instantly
- ✅ **All from Telegram** - no website needed!

---

## 🚀 **Setup Instructions**

### **Step 1: Set Webhook (One Time Setup)**

After starting your server, visit this URL to set up the webhook:

```
http://127.0.0.1:8000/api/telegram/set-webhook/
```

Or manually set it:
```
http://127.0.0.1:8000/api/telegram/set-webhook/?url=http://your-domain.com/api/telegram/webhook/
```

**For production**, use your actual domain:
```
https://yourdomain.com/api/telegram/set-webhook/
```

---

### **Step 2: Add Employees to Telegram Group**

1. **Create a Telegram group** for your employees
2. **Add your bot** to the group (search for your bot name)
3. **Get the group chat ID:**
   - Add `@getidsbot` to your group
   - It will show the group chat ID (like `-123456789`)
   - Update `TELEGRAM_CHAT_ID` in settings.py with this ID

---

### **Step 3: Update Settings (Optional)**

If you want to use a different chat ID for employee notifications:

```python
# In project/settings.py
TELEGRAM_EMPLOYEE_CHAT_ID = os.environ.get('TELEGRAM_EMPLOYEE_CHAT_ID', '-4974214796')
```

---

## 📱 **How Employees Use It**

### **Commands Available:**

#### **1. `/start` or `/help`**
Shows all available commands

#### **2. `/orders`**
View all orders that need preparation (pending/confirmed)

#### **3. `/preparing`**
View orders currently being prepared

#### **4. `/ready`**
View orders ready for delivery

#### **5. `/out`**
View orders out for delivery

#### **6. `/order MD00001`**
View specific order details (replace MD00001 with order number)

---

## 🎯 **Interactive Buttons**

When a new order comes in, employees see a message with buttons:

### **For New Orders:**
- **👷 Start Preparing** - Updates status to "Preparing"
- **📋 View Details** - Opens order in employee dashboard

### **For Preparing Orders:**
- **📦 Mark Ready** - Updates status to "Ready for Delivery"
- **🖨️ Get QR Code Link** - Shows QR code print page (COD only)
- **📋 View Details** - Opens order details

### **For Ready Orders:**
- **🚚 Out for Delivery** - Updates status to "Out for Delivery"
- **📋 View Details** - Opens order details

### **For Out for Delivery:**
- **✅ Mark Delivered** - Updates status to "Delivered"
- **📋 View Details** - Opens order details

---

## 💡 **Example Workflow**

### **Scenario: New Order Comes In**

1. **Employee receives notification** in Telegram:
   ```
   🛒 NEW ORDER RECEIVED!
   
   📦 Order #MD00001
   👤 Customer: John Doe
   📱 Phone: 012345678
   💵 Total: $50.00
   ```

2. **Employee clicks "👷 Start Preparing"** button
   - Status automatically updates to "Preparing"
   - Employee prepares the order

3. **If COD order**, employee clicks **"🖨️ Get QR Code Link"**
   - Gets link to print QR code
   - Prints and attaches to order

4. **Employee clicks "📦 Mark Ready"**
   - Status updates to "Ready for Delivery"
   - Order ready for driver pickup

5. **Driver picks up**, employee clicks **"🚚 Out for Delivery"**
   - Status updates to "Out for Delivery"

6. **After delivery**, employee clicks **"✅ Mark Delivered"**
   - Status updates to "Delivered"
   - Order complete!

---

## 🔧 **Testing**

### **Test Commands:**

1. **Send `/start`** to your bot
   - Should receive help message

2. **Send `/orders`**
   - Should see pending orders

3. **Place a test order** on website
   - Should receive notification with buttons

4. **Click buttons** on notification
   - Should update order status

---

## 📋 **What Employees See**

### **New Order Notification:**
```
🛒 NEW ORDER RECEIVED!

📦 Order #MD00001

⏳ Status: Pending
💰 Payment: Cash on Delivery

👤 Customer:
   Name: John Doe
   Phone: 012345678
   Address: Street 123
   Province: Phnom Penh

💰 Total: $50.00
⏰ Time: 2024-01-15 14:30

[👷 Start Preparing] [📋 View Details]
```

### **Order Details Command:**
```
📦 Order #MD00001

👷 Status: Preparing
💰 Payment: Cash on Delivery

👤 Customer:
   Name: John Doe
   Phone: 012345678
   Address: Street 123
   Province: Phnom Penh

  • Product 1 x2 = $30.00
  • Product 2 x1 = $20.00

💰 Total: $50.00
⏰ Time: 2024-01-15 14:30

⏳ Payment: Pending

[📦 Mark Ready] [🖨️ Get QR Code Link] [📋 View Details]
```

---

## 🎉 **Benefits**

### **For Employees:**
- ✅ No need to open website
- ✅ Instant notifications
- ✅ Quick status updates
- ✅ Works on mobile phones
- ✅ Easy to use

### **For You (Admin):**
- ✅ Employees can work from anywhere
- ✅ Faster order processing
- ✅ Better communication
- ✅ Real-time updates
- ✅ Less manual work

---

## 🔒 **Security Note**

The webhook endpoint is currently open. For production:

1. **Add authentication** to webhook
2. **Use HTTPS** only
3. **Verify Telegram secret token**
4. **Rate limiting** (already implemented)

---

## 🚀 **Ready to Use!**

1. **Start your server:**
   ```bash
   python manage.py runserver
   ```

2. **Set webhook:**
   ```
   http://127.0.0.1:8000/api/telegram/set-webhook/
   ```

3. **Add employees to Telegram group**

4. **Start using!** Send `/start` to your bot

---

## 📞 **Need Help?**

- Check server logs for errors
- Verify bot token is correct
- Make sure webhook is set
- Test with `/start` command first

**Your employees can now manage orders instantly from Telegram!** 🎉

