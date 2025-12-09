# MADAM DA - E-commerce Website

## 🚀 Quick Start

### **Start Server:**
Double-click: `START_SERVER_WEBSOCKET.bat`

### **Access:**
- **Customer Website:** http://127.0.0.1:8000/
- **Employee Dashboard:** http://127.0.0.1:8000/employee/
- **Admin Panel:** http://127.0.0.1:8000/admin/

---

## 📋 Features

- ✅ E-commerce shop with products
- ✅ KHQR payment integration
- ✅ Cash on Delivery (COD) with QR code confirmation
- ✅ Real-time employee dashboard with WebSocket
- ✅ Telegram bot for order notifications
- ✅ Order management system
- ✅ Sales and commission reports
- ✅ Promoter commission tracking

---

## 🔧 Setup

### **Requirements:**
- Python 3.8+
- Redis (for WebSocket)
- Django 5.2+

### **Install:**
```bash
pip install -r requirements.txt
```

### **Start Redis:**
Redis should run automatically as Windows service.

### **Run Migrations:**
```bash
python manage.py migrate
```

### **Start Server:**
```bash
START_SERVER_WEBSOCKET.bat
```

---

## 📚 Documentation

- **How to Start Server:** `HOW_TO_START_SERVER.md`
- **Full Workflow:** `FULL_WORKFLOW_EXPLAINED.md`
- **Telegram Bot Setup:** `TELEGRAM_BOT_SETUP.md`

---

## 🎯 Main Features

### **For Customers:**
- Browse products
- Add to cart
- Checkout with payment options (KHQR or COD)

### **For Employees:**
- Real-time dashboard
- View orders instantly
- Update order status
- Print QR codes for COD

### **For Admin:**
- Full order management
- Sales reports
- Commission tracking
- Order verification

---

## 📞 Support

For issues or questions, check the documentation files.

---

**Built with Django + Channels + Redis + Telegram Bot**
