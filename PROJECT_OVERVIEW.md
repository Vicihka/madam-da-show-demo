# 🛍️ MADAM DA - E-Commerce Platform Overview

## 📋 Project Summary

**MADAM DA** is a full-featured Django-based e-commerce platform designed for a beauty products business. The system supports both English and Khmer languages, handles multiple payment methods (KHQR, Cash on Delivery), includes real-time order management, and is optimized to handle **1000+ concurrent customers**.

---

## 🎯 What This Project Does

This is a **complete e-commerce solution** that allows:
- **Customers** to browse products, place orders, and track their purchases
- **Employees** to manage orders in real-time through a dashboard
- **Administrators** to manage products, view sales reports, and track commissions

---

## 🏗️ Project Structure

### **Core Components:**

1. **Django Backend** (`app/`)
   - Models: Products, Orders, Customers, Promo Codes, etc.
   - Views: Shop, Checkout, Order Management, APIs
   - Admin: Full admin panel with import/export
   - WebSocket: Real-time order updates

2. **Frontend** (`templates/`, `static/`)
   - Customer-facing shop pages
   - Employee dashboard
   - Responsive design for mobile/desktop

3. **Database**
   - PostgreSQL (production-ready)
   - SQLite (development fallback)
   - Optimized with indexes for performance

4. **Real-Time Features**
   - WebSocket connections (Django Channels)
   - Redis for caching and channel layers

---

## ✨ Key Features

### **1. Customer Features**

#### **Shopping Experience:**
- ✅ **Bilingual Support**: English and Khmer language switching
- ✅ **Product Catalog**: Browse products with images, prices, descriptions
- ✅ **Hero Carousel**: Image/video slides on homepage
- ✅ **Shopping Cart**: Add/remove items, quantity management
- ✅ **Product Search & Filter**: Find products easily
- ✅ **Responsive Design**: Works on mobile, tablet, desktop

#### **Checkout & Payment:**
- ✅ **KHQR Payment**: Generate QR codes for mobile payment
- ✅ **Cash on Delivery (COD)**: Order now, pay on delivery
- ✅ **Promo Codes**: Apply discount codes
- ✅ **Referral System**: Earn points for referrals
- ✅ **Loyalty Points**: Earn and redeem loyalty points
- ✅ **Order Tracking**: Track order status by phone number

#### **Order Management:**
- ✅ **Order Confirmation**: Receipt with order details
- ✅ **Download Receipt**: Save receipt as PNG image
- ✅ **Order History**: View past orders
- ✅ **Customer Lookup**: Find orders by phone number

### **2. Employee Dashboard Features**

#### **Real-Time Order Management:**
- ✅ **Live Updates**: WebSocket-powered real-time order notifications
- ✅ **Order Status Tracking**: 
  - Pending → Confirmed → Preparing → Ready → Out for Delivery → Delivered
- ✅ **Order Cards**: Visual cards showing order details
- ✅ **Status Updates**: Change order status with one click
- ✅ **COD Payment Confirmation**: Mark COD payments as received
- ✅ **QR Code Printing**: Print QR codes for COD confirmation
- ✅ **Order Details View**: Full order information
- ✅ **Customer Received Tracking**: Mark when customer receives order

#### **Dashboard Sections:**
- **To Prepare**: New orders that need action
- **Preparing**: Orders currently being prepared
- **Ready for Delivery**: Orders ready to ship
- **Out for Delivery**: Orders in transit
- **Delivered**: Completed orders (last 7 days)

### **3. Admin Panel Features**

#### **Product Management:**
- ✅ **CRUD Operations**: Create, read, update, delete products
- ✅ **Bilingual Content**: English and Khmer names/descriptions
- ✅ **Image Upload**: Product images with validation
- ✅ **Stock Management**: Track inventory levels
- ✅ **Bulk Import/Export**: Excel/CSV import/export with Khmer support
- ✅ **Product Badges**: "New", "Sale", "Popular" badges

#### **Order Management:**
- ✅ **Order List**: View all orders with filters
- ✅ **Order Details**: Full order information
- ✅ **Status Management**: Change order status
- ✅ **Payment Tracking**: Track COD payments
- ✅ **Order Verification**: Verify suspicious orders
- ✅ **Customer Received Tracking**: Track delivery confirmation

#### **Sales & Reports:**
- ✅ **Sales Dashboard**: Revenue, order counts, trends
- ✅ **Commission Reports**: Track promoter commissions
- ✅ **Date Range Filtering**: Filter by date ranges
- ✅ **Export Reports**: Export data to Excel/CSV

#### **Promoter Management:**
- ✅ **Promoter CRUD**: Create and manage promoters
- ✅ **Commission Tracking**: Track commission rates and earnings
- ✅ **Promo Code Assignment**: Assign promo codes to promoters
- ✅ **Revenue Reports**: View promoter revenue

#### **Customer Management:**
- ✅ **Customer List**: View all customers
- ✅ **Customer Details**: View customer orders and history
- ✅ **Loyalty Points**: Track loyalty point transactions
- ✅ **Referral Tracking**: Track referral activities

#### **Content Management:**
- ✅ **Hero Slides**: Manage homepage carousel slides
- ✅ **Newsletter**: Manage newsletter subscriptions
- ✅ **Promo Codes**: Create and manage discount codes

### **4. Technical Features**

#### **Performance & Scalability:**
- ✅ **Pagination**: Products paginated (20 per page)
- ✅ **Caching**: Redis caching for production
- ✅ **Database Indexes**: Optimized queries for 1000+ customers
- ✅ **Query Optimization**: `select_related` and `prefetch_related`
- ✅ **Connection Pooling**: PostgreSQL connection pooling
- ✅ **Rate Limiting**: API rate limiting (production)
- ✅ **WebSocket Limits**: Max 100 concurrent connections

#### **Security:**
- ✅ **CSRF Protection**: Django CSRF tokens
- ✅ **XSS Protection**: Content Security Policy (CSP)
- ✅ **SQL Injection Protection**: Django ORM
- ✅ **File Upload Validation**: Image/video validation
- ✅ **Request Size Limits**: Prevent large uploads
- ✅ **Security Headers**: Security middleware
- ✅ **HTTPS Support**: SSL redirect (production)
- ✅ **Environment Variables**: Secure configuration

#### **Multi-Language Support:**
- ✅ **English & Khmer**: Full bilingual support
- ✅ **UTF-8 Encoding**: Proper Khmer text rendering
- ✅ **Google Fonts**: Khmer fonts (Dangrek, AkbalthomMonstera)
- ✅ **Language Switching**: Easy language toggle

#### **Payment Integration:**
- ✅ **KHQR API**: Bakong payment integration
- ✅ **QR Code Generation**: Generate payment QR codes
- ✅ **Payment Status Checking**: Poll payment status
- ✅ **COD Automation**: QR code confirmation for COD

#### **Notifications:**
- ✅ **Telegram Bot**: Order notifications via Telegram
- ✅ **Interactive Buttons**: Telegram bot with action buttons
- ✅ **WebSocket Notifications**: Real-time browser notifications

---

## 📁 File Structure

```
DJANGO - MADAM DA/
├── app/                          # Main Django application
│   ├── models.py                 # Database models (Product, Order, Customer, etc.)
│   ├── views.py                  # Customer-facing views and APIs
│   ├── employee_views.py         # Employee dashboard views
│   ├── admin.py                  # Admin panel configuration
│   ├── consumers.py              # WebSocket consumers
│   ├── middleware.py             # Custom middleware (security, compression)
│   ├── routing.py                # WebSocket routing
│   ├── telegram_bot.py           # Telegram bot integration
│   ├── telegram_webhook.py       # Telegram webhook handler
│   └── migrations/               # Database migrations
│
├── project/                      # Django project settings
│   ├── settings.py              # Main configuration
│   ├── urls.py                   # URL routing
│   ├── asgi.py                   # ASGI config (WebSocket)
│   └── wsgi.py                   # WSGI config
│
├── templates/                    # HTML templates
│   ├── app/
│   │   ├── index.html           # Shop homepage
│   │   ├── checkout.html        # Checkout page
│   │   ├── order_success.html   # Order confirmation
│   │   ├── employee_dashboard.html  # Employee dashboard
│   │   └── ...                  # Other pages
│   └── admin/                   # Admin templates
│
├── static/                       # Static files
│   ├── css/                     # Stylesheets
│   ├── js/                      # JavaScript files
│   └── images/                  # Images (logos, etc.)
│
├── media/                        # User-uploaded files
│   ├── products/                # Product images
│   ├── hero_slides/             # Hero carousel images
│   └── qr_codes/               # Generated QR codes
│
├── requirements.txt              # Python dependencies
├── manage.py                     # Django management script
├── .env                          # Environment variables
└── README.md                     # Quick start guide
```

---

## 🗄️ Database Models

### **Core Models:**

1. **Product**
   - Product information (name, price, image, stock)
   - Bilingual support (English/Khmer)
   - Badges, descriptions, inventory

2. **Customer**
   - Customer information (name, phone, address)
   - Loyalty points, referral codes
   - No login required (phone-based)

3. **Order**
   - Order details (customer, items, totals)
   - Status tracking (pending → delivered)
   - Payment method, COD tracking
   - Verification and suspicious order flags

4. **OrderItem**
   - Individual items in an order
   - Product reference, quantity, price

5. **PromoCode**
   - Discount codes
   - Percentage or fixed discounts
   - Usage limits, validity dates
   - Promoter association

6. **Promoter**
   - Promoter information
   - Commission rates
   - Revenue tracking

7. **OrderQRCode**
   - QR codes for KHQR payments
   - Expiration tracking (10 minutes)
   - Payment status

8. **HeroSlide**
   - Homepage carousel slides
   - Image/video/URL support

9. **Newsletter**
   - Newsletter subscriptions

10. **Referral**
    - Referral tracking
    - Reward points

11. **LoyaltyPoint**
    - Loyalty point transactions
    - Earned/used/expired tracking

---

## 🔌 API Endpoints

### **Customer APIs:**
- `GET /` - Shop homepage
- `GET /checkout/` - Checkout page
- `GET /order/success/` - Order confirmation
- `GET /track-order/` - Order tracking page
- `POST /api/customer/lookup/` - Find customer by phone
- `POST /api/promo/validate/` - Validate promo code
- `POST /api/referral/check/` - Check referral code
- `POST /api/loyalty/calculate/` - Calculate loyalty points
- `POST /api/khqr/create/` - Create KHQR payment
- `POST /api/khqr/check/` - Check payment status
- `POST /api/order/create-on-payment/` - Create order after payment
- `POST /api/order/track/` - Track order by phone
- `POST /api/newsletter/subscribe/` - Subscribe to newsletter

### **Employee APIs:**
- `GET /employee/` - Employee dashboard
- `GET /employee/api/` - Dashboard API (JSON)
- `GET /employee/order/<order_number>/` - Order details
- `POST /api/employee/order/<order_number>/status/` - Update order status
- `POST /api/employee/order/<order_number>/confirm-payment/` - Confirm COD payment

### **COD APIs:**
- `GET /cod/confirm/` - COD confirmation page
- `GET /cod/qr/<order_number>/` - COD QR code
- `GET /cod/print/<order_number>/` - COD print view
- `POST /api/cod/confirm/` - Confirm COD order

### **System APIs:**
- `GET /health/` - Health check endpoint
- `GET /api/health/` - Health check API
- `POST /api/telegram/webhook/` - Telegram webhook

---

## 🚀 How It Works

### **Customer Order Flow:**

1. **Browse Products** → Customer views products on homepage
2. **Add to Cart** → Items added to shopping cart
3. **Checkout** → Customer enters shipping information
4. **Payment**:
   - **KHQR**: Generate QR code → Customer scans → Payment confirmed → Order created
   - **COD**: Order created immediately → QR code generated for confirmation
5. **Order Confirmation** → Receipt shown, can download as image
6. **Order Tracking** → Customer can track order by phone number

### **Employee Workflow:**

1. **Dashboard Opens** → WebSocket connects for real-time updates
2. **New Order Arrives** → Order appears in "To Prepare" section
3. **Update Status** → Employee clicks to change status:
   - Pending → Confirmed → Preparing → Ready → Out for Delivery → Delivered
4. **COD Payment** → Employee confirms payment received
5. **Print QR Code** → Print QR code for COD confirmation
6. **Customer Received** → Mark when customer receives order

### **Admin Workflow:**

1. **Product Management** → Add/edit products in admin panel
2. **Order Management** → View all orders, change status, verify orders
3. **Sales Reports** → View revenue, commissions, trends
4. **Promoter Management** → Create promoters, assign promo codes
5. **Bulk Import** → Import products from Excel/CSV

---

## 🛠️ Technologies Used

- **Backend**: Django 5.2.9
- **Database**: PostgreSQL (production), SQLite (development)
- **Real-Time**: Django Channels (WebSocket)
- **Caching**: Redis
- **Payment**: Bakong KHQR API
- **Notifications**: Telegram Bot API
- **Frontend**: HTML, CSS, JavaScript
- **Libraries**:
  - `html2canvas` - Receipt image generation
  - `qrcode` - QR code generation
  - `django-ratelimit` - Rate limiting
  - `django-cors-headers` - CORS handling
  - `django-import-export` - Excel/CSV import/export
  - `channels-redis` - Redis channel layer
  - `whitenoise` - Static file serving
  - `gunicorn` - WSGI server
  - `daphne` - ASGI server

---

## ⚙️ Configuration

### **Environment Variables (.env):**

```env
# Debug Mode
DEBUG=True                    # Development: True, Production: False

# Security
SECRET_KEY=your-secret-key    # Required in production
ALLOWED_HOSTS=127.0.0.1,localhost,*  # Comma-separated hosts

# Database (PostgreSQL)
DB_NAME=madamda
DB_USER=postgres
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://127.0.0.1:6379/1

# Bakong Payment
BAKONG_ID=your-bakong-id
BAKONG_MERCHANT_NAME=MADAM DA

# Telegram Bot
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id

# SSL (Production)
ENABLE_SSL_REDIRECT=False    # Set to True in production with HTTPS
```

---

## 📊 Scalability Features

### **Optimized for 1000+ Customers:**

1. **Database:**
   - PostgreSQL with connection pooling
   - Database indexes on frequently queried fields
   - Query optimization (`select_related`, `prefetch_related`)

2. **Caching:**
   - Redis caching for products and hero slides
   - Session caching in production

3. **Pagination:**
   - Products paginated (20 per page)
   - Order queries limited (100 per status)

4. **WebSocket:**
   - Connection limit (100 concurrent)
   - Efficient message broadcasting

5. **Static Files:**
   - WhiteNoise for static file serving
   - Browser caching headers

6. **Rate Limiting:**
   - API rate limiting in production
   - Request size limits

---

## 🔒 Security Features

- ✅ CSRF protection
- ✅ XSS protection (CSP headers)
- ✅ SQL injection protection (Django ORM)
- ✅ File upload validation
- ✅ Request size limits
- ✅ Security headers middleware
- ✅ HTTPS support (production)
- ✅ Environment variable configuration
- ✅ Admin URL customization
- ✅ Suspicious order detection

---

## 📱 Mobile Support

- ✅ Responsive design (mobile-first)
- ✅ Touch-friendly interface
- ✅ Mobile-optimized checkout
- ✅ QR code scanning support
- ✅ Receipt download works on mobile

---

## 🌐 Multi-Language Support

- ✅ English and Khmer languages
- ✅ Language switching
- ✅ UTF-8 encoding
- ✅ Khmer fonts (Google Fonts)
- ✅ Bilingual product names/descriptions
- ✅ Proper Khmer text rendering in receipts

---

## 📈 Monitoring & Health Checks

- ✅ Health check endpoint (`/health/`)
- ✅ Database connection monitoring
- ✅ Cache status monitoring
- ✅ Logging system (Django logs, security logs)

---

## 🎨 UI/UX Features

- ✅ Modern, clean design
- ✅ Hero carousel with images/videos
- ✅ Product cards with images
- ✅ Shopping cart with quantity controls
- ✅ Order status cards (employee dashboard)
- ✅ Real-time updates (WebSocket)
- ✅ Loading states and animations
- ✅ Error handling and user feedback

---

## 📝 Documentation Files

- `README.md` - Quick start guide
- `DEBUG_MODE_GUIDE.md` - Debug mode configuration
- `QUICK_DEBUG_SWITCH.md` - Quick debug switching
- `TELEGRAM_BOT_SETUP.md` - Telegram bot setup
- `SCALABILITY_REVIEW_1000_PLUS_CUSTOMERS.md` - Scalability review
- `PROJECT_OVERVIEW.md` - This file

---

## 🚦 Getting Started

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Database:**
   - Configure PostgreSQL in `.env`
   - Run migrations: `python manage.py migrate`

3. **Start Redis:**
   - Redis must be running for WebSocket

4. **Start Server:**
   - Development: `python manage.py runserver`
   - Production: Use `daphne` or `gunicorn`

5. **Access:**
   - Customer: http://127.0.0.1:8000/
   - Employee: http://127.0.0.1:8000/employee/
   - Admin: http://127.0.0.1:8000/admin/

---

## ✅ What's Working

- ✅ Full e-commerce functionality
- ✅ Bilingual support (English/Khmer)
- ✅ Multiple payment methods (KHQR, COD)
- ✅ Real-time order management
- ✅ Employee dashboard
- ✅ Admin panel with reports
- ✅ Order tracking
- ✅ Receipt download
- ✅ Telegram notifications
- ✅ Scalability optimizations
- ✅ Security features
- ✅ Mobile responsive design

---

## 🎯 Use Cases

1. **Beauty Products E-Commerce**: Primary use case
2. **Order Management System**: For employees
3. **Sales & Commission Tracking**: For administrators
4. **Customer Loyalty Program**: Referrals and points
5. **Multi-Payment Gateway**: KHQR and COD

---

## 📞 Support

For issues or questions:
- Check documentation files in project root
- Review error logs in `logs/` directory
- Check Django admin panel for data issues

---

**Built with ❤️ using Django, Channels, Redis, and PostgreSQL**

