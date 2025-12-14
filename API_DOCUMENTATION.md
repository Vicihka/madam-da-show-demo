# 📚 MADAM DA E-Commerce API Documentation

## 🌐 Base URL

- **Development:** `http://127.0.0.1:8000`
- **Production:** `https://yourdomain.com`

---

## 📋 Table of Contents

1. [Customer APIs](#customer-apis)
2. [Order APIs](#order-apis)
3. [Employee APIs](#employee-apis)
4. [Payment APIs](#payment-apis)
5. [System APIs](#system-apis)
6. [Error Responses](#error-responses)

---

## 👤 Customer APIs

### 1. Customer Lookup

**Endpoint:** `GET /api/customer/lookup/`

**Description:** Look up customer information by phone number for auto-filling checkout form.

**Query Parameters:**
- `phone` (required): Phone number to lookup

**Example Request:**
```bash
GET /api/customer/lookup/?phone=012345678
```

**Success Response (200):**
```json
{
  "success": true,
  "customer": {
    "name": "John Doe",
    "phone": "012345678",
    "address": "123 Test Street",
    "province": "Phnom Penh"
  }
}
```

**Error Response (400):**
```json
{
  "success": false,
  "message": "Phone number is required"
}
```

**Error Response (200 - Not Found):**
```json
{
  "success": false,
  "message": "Customer not found"
}
```

---

### 2. Validate Promo Code

**Endpoint:** `POST /api/promo/validate/`

**Description:** Validate and calculate discount for a promo code.

**Request Body:**
```json
{
  "code": "SAVE10",
  "amount": 100.00
}
```

**Success Response (200):**
```json
{
  "success": true,
  "code": "SAVE10",
  "discount_amount": 10.00,
  "discount_type": "percentage",
  "discount_value": 10.00,
  "message": "Discount applied: $10.00"
}
```

**Error Responses:**
- **400:** Invalid JSON, missing fields, below minimum purchase
- **404:** Promo code not found or inactive
- **500:** Server error

---

### 3. Check Referral Code

**Endpoint:** `POST /api/referral/check/`

**Description:** Validate a referral code.

**Request Body:**
```json
{
  "code": "MD123456"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Valid referral code"
}
```

**Error Response (404):**
```json
{
  "success": false,
  "message": "Invalid referral code"
}
```

---

### 4. Calculate Loyalty Points

**Endpoint:** `POST /api/loyalty/calculate/`

**Description:** Calculate loyalty points for an order amount.

**Request Body:**
```json
{
  "amount": 100.00
}
```

**Success Response (200):**
```json
{
  "success": true,
  "points": 10,
  "message": "You will earn 10 loyalty points"
}
```

---

### 5. Newsletter Subscribe

**Endpoint:** `POST /api/newsletter/subscribe/`

**Description:** Subscribe to newsletter.

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "phone": "012345678"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Successfully subscribed to newsletter"
}
```

**Error Response (400):**
```json
{
  "success": false,
  "message": "Email is required"
}
```

---

## 📦 Order APIs

### 6. Track Order

**Endpoint:** `POST /api/order/track/`

**Description:** Track order status by order number and phone number.

**Request Body:**
```json
{
  "order_number": "MD00001",
  "phone": "012345678"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "order": {
    "order_number": "MD00001",
    "status": "preparing",
    "status_display": "Preparing",
    "customer_name": "John Doe",
    "customer_phone": "012345678",
    "customer_address": "123 Test Street",
    "customer_province": "Phnom Penh",
    "total": "50.00",
    "payment_method": "Cash on Delivery",
    "created_at": "2024-01-15T10:30:00Z",
    "items": [
      {
        "product_name": "Product Name",
        "quantity": 2,
        "product_price": "25.00",
        "subtotal": "50.00"
      }
    ]
  }
}
```

**Error Responses:**
- **400:** Missing required fields
- **403:** Phone number doesn't match order
- **404:** Order not found
- **500:** Server error

---

### 7. Create Order on Payment

**Endpoint:** `POST /api/order/create-on-payment/`

**Description:** Create order after successful payment (KHQR).

**Request Body:**
```json
{
  "payment_id": "payment_123",
  "customer_name": "John Doe",
  "customer_phone": "012345678",
  "customer_email": "john@example.com",
  "customer_address": "123 Test Street",
  "customer_province": "Phnom Penh",
  "items": [
    {
      "product_id": "PROD001",
      "quantity": 2,
      "price": 25.00
    }
  ],
  "subtotal": 50.00,
  "shipping_fee": 0.00,
  "discount_amount": 0.00,
  "total": 50.00,
  "payment_method": "KHQR",
  "promo_code": null,
  "referral_code": null,
  "loyalty_points_used": 0
}
```

**Success Response (200):**
```json
{
  "success": true,
  "order_number": "MD00001",
  "message": "Order created successfully"
}
```

---

## 💳 Payment APIs

### 8. Create KHQR Payment

**Endpoint:** `POST /api/khqr/create/`

**Description:** Create KHQR payment QR code.

**Request Body:**
```json
{
  "amount": 50.00,
  "description": "Order payment",
  "customer_name": "John Doe",
  "customer_phone": "012345678"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "qr_code_url": "/media/qr_codes/order_123.png",
  "qr_data": "khqr://...",
  "order_number": "MD00001",
  "expires_at": "2024-01-15T10:40:00Z"
}
```

**Error Response (400/500):**
```json
{
  "success": false,
  "message": "Error message"
}
```

---

### 9. Check Payment Status

**Endpoint:** `POST /api/khqr/check/`

**Description:** Check if payment has been confirmed.

**Request Body:**
```json
{
  "payment_id": "payment_123"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "paid": true,
  "payment_time": "2024-01-15T10:35:00Z"
}
```

**Not Paid Response (200):**
```json
{
  "success": true,
  "paid": false
}
```

---

### 10. COD Confirm API

**Endpoint:** `POST /api/cod/confirm/`

**Description:** Confirm Cash on Delivery order (used by QR scanner).

**Request Body:**
```json
{
  "order_number": "MD00001"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Order confirmed",
  "order": {
    "order_number": "MD00001",
    "status": "confirmed"
  }
}
```

---

## 👔 Employee APIs

### 11. Employee Dashboard API

**Endpoint:** `GET /employee/api/`

**Description:** Get dashboard data in JSON format.

**Success Response (200):**
```json
{
  "orders_to_prepare": [...],
  "orders_preparing": [...],
  "orders_ready": [...],
  "orders_out": [...],
  "orders_delivered": [...]
}
```

---

### 12. Update Order Status

**Endpoint:** `POST /api/employee/order/<order_number>/status/`

**Description:** Update order status.

**Request Body:**
```json
{
  "status": "preparing"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Order status updated",
  "order": {
    "order_number": "MD00001",
    "status": "preparing"
  }
}
```

**Valid Status Values:**
- `pending`
- `confirmed`
- `preparing`
- `ready_for_delivery`
- `out_for_delivery`
- `delivered`
- `cancelled`

---

### 13. Confirm COD Payment

**Endpoint:** `POST /api/employee/order/<order_number>/confirm-payment/`

**Description:** Confirm payment received for COD order.

**Request Body:**
```json
{
  "payment_received": true,
  "notes": "Payment received in cash"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Payment confirmed",
  "order": {
    "order_number": "MD00001",
    "payment_received": true
  }
}
```

---

## 🔧 System APIs

### 14. Health Check

**Endpoint:** `GET /health/` or `GET /api/health/`

**Description:** Check system health (database, cache, etc.).

**Success Response (200):**
```json
{
  "status": "ok",
  "database": "ok",
  "cache": "ok",
  "cache_type": "redis",
  "debug_mode": false,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Degraded Response (200):**
```json
{
  "status": "degraded",
  "database": "ok",
  "cache": "error",
  "cache_type": "dummy (development)",
  "debug_mode": true,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### 15. Telegram Webhook

**Endpoint:** `POST /api/telegram/webhook/`

**Description:** Webhook endpoint for Telegram bot updates.

**Request Body:** (Telegram Update object)
```json
{
  "update_id": 123456,
  "message": {
    "message_id": 1,
    "from": {...},
    "chat": {...},
    "text": "..."
  }
}
```

**Success Response (200):**
```json
{
  "ok": true
}
```

---

## ❌ Error Responses

### Standard Error Format

All error responses follow this format:

```json
{
  "success": false,
  "message": "Error description"
}
```

### HTTP Status Codes

- **200:** Success (even for "not found" cases in some APIs)
- **400:** Bad Request (missing/invalid parameters)
- **403:** Forbidden (unauthorized access)
- **404:** Not Found (resource doesn't exist)
- **500:** Internal Server Error

### Common Error Messages

- `"Phone number is required"`
- `"Order number and phone number are required"`
- `"Invalid promo code"`
- `"Promo code has expired"`
- `"Minimum order amount is $X"`
- `"Phone number does not match this order"`
- `"Order not found"`
- `"Invalid JSON data"`
- `"An error occurred. Please try again."`

---

## 🔒 Authentication & Security

### CSRF Protection

Most POST endpoints require CSRF token. Include in headers:
```
X-CSRFToken: <token>
```

Or use `@csrf_exempt` endpoints (marked in code).

### Rate Limiting

Some endpoints have rate limiting:
- Customer Lookup: 60 requests/minute
- Promo Code Validation: 30 requests/minute
- Order Tracking: 60 requests/minute

---

## 📝 Notes

1. **Phone Number Format:** Phone numbers are normalized (spaces/dashes removed)
2. **Order Numbers:** Format is `MD#####` (e.g., `MD00001`)
3. **Currency:** All amounts are in USD (decimal format)
4. **Dates:** ISO 8601 format (UTC)
5. **Language:** Supports English and Khmer (Khmer text in UTF-8)

---

## 🧪 Testing

Run unit tests:
```bash
python manage.py test app.tests
```

Test specific test class:
```bash
python manage.py test app.tests.CustomerLookupAPITest
```

---

**Last Updated:** 2024-01-15
**API Version:** 1.0

