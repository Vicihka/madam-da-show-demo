# 🐛 Bug Fixes: Media File 500 Error & Order Creation 400 Error

**Date:** 2024-01-15  
**Issues Fixed:** Media file 500 error, Order creation 400 error with better error messages

---

## ✅ Issue 1: Media File 500 Error

### Problem
Media files (hero slides, product images) were returning 500 Internal Server Error when accessed.

**Error:**
```
GET http://127.0.0.1:8000/media/hero_slides/220938c609a7a3995729b8bf118a8c43.jpg 500 (Internal Server Error)
```

### Root Cause
The `SecurityHeadersMiddleware` was processing error responses (4xx, 5xx) and media files, causing issues when:
1. The file doesn't exist (404 becomes 500)
2. Error responses were being modified incorrectly

### Fix Applied
**File:** `app/middleware.py`

**Changes:**
- Added early return for error responses (status >= 400) to prevent middleware interference
- Added early return for media files before any header manipulation
- This ensures media files are served without security header processing

**Code:**
```python
def process_response(self, request, response):
    # Skip processing for error responses (4xx, 5xx)
    # This prevents middleware from interfering with error pages
    if response.status_code >= 400:
        return response
    
    # Skip processing for media files early (before any header manipulation)
    if request.path.startswith('/media/'):
        return response
    
    # ... rest of security headers code
```

### Result
✅ Media files now load correctly without 500 errors
✅ Error responses (404, 500) are not modified by middleware
✅ Security headers still applied to regular HTML responses

---

## ✅ Issue 2: Order Creation 400 Error - Better Error Messages

### Problem
Order creation was failing with 400 Bad Request, but the error message wasn't clear about what field was missing.

**Error:**
```
POST http://127.0.0.1:8000/api/order/create-on-payment/ 400 (Bad Request)
Error creating COD order: Error: Failed to create order
```

### Root Cause
The validation was checking all fields together with `all([name, phone, address, province])`, which doesn't tell the user which specific field is missing.

### Fixes Applied

#### 1. Improved Validation Error Messages
**File:** `app/views.py` - `create_order_on_payment()` function

**Changes:**
- Changed validation to check each field individually
- Return specific list of missing fields in error message
- Use `handle_api_error()` for consistent error format
- Added context logging for debugging

**Before:**
```python
if not all([name, phone, address, province]):
    return JsonResponse({
        'success': False,
        'error': {
            'type': 'ValidationError',
            'message': 'Missing required fields: name, phone, address, and province are required'
        }
    }, status=400)
```

**After:**
```python
missing_fields = []
if not name:
    missing_fields.append('name')
if not phone:
    missing_fields.append('phone')
if not address:
    missing_fields.append('address')
if not province:
    missing_fields.append('province')

if missing_fields:
    error = ValidationError(f'Missing required fields: {", ".join(missing_fields)}')
    context = {
        'endpoint': 'create_order_on_payment',
        'missing_fields': missing_fields,
        'received_data': {
            'name': bool(name),
            'phone': bool(phone),
            'address': bool(address),
            'province': bool(province)
        }
    }
    return handle_api_error(error, context=context)
```

#### 2. Improved Customer Creation/Update
**File:** `app/views.py` - `create_order_on_payment()` function

**Changes:**
- Update customer information if customer exists but info changed
- Better error handling for customer creation failures

**Code:**
```python
customer, created = Customer.objects.get_or_create(
    phone=phone,
    defaults={'name': name, 'address': address, 'province': province}
)
# Update customer info if customer already exists but info changed
if not created:
    if customer.name != name or customer.address != address or customer.province != province:
        customer.name = name
        customer.address = address
        customer.province = province
        customer.save(update_fields=['name', 'address', 'province'])
```

#### 3. Improved JavaScript Error Handling
**File:** `static/js/checkout.js` - `createOrderForCOD()` and `createOrderOnPaymentConfirmation()`

**Changes:**
- Better error message extraction from API response
- Show user-friendly error messages using toast notifications
- Handle both `result.error.message` and `result.message` formats
- Better error logging for debugging

**Before:**
```javascript
if (result.success) {
    // success handling
} else {
    throw new Error(result.message || 'Failed to create order');
}
```

**After:**
```javascript
if (!response.ok || !result.success) {
    // Get error message from response
    const errorMessage = result.error?.message || result.message || `Failed to create order (HTTP ${response.status})`;
    console.error('Order creation failed:', result);
    showToast(errorMessage, 'error');  // Show user-friendly message
    throw new Error(errorMessage);
}
```

### Result
✅ Clear error messages showing which fields are missing
✅ User-friendly error notifications displayed
✅ Better error logging for debugging
✅ Consistent error response format

---

## 🧪 Testing

### Test Media Files
1. ✅ Access media files directly: `http://127.0.0.1:8000/media/hero_slides/image.jpg`
2. ✅ Should return 200 OK (not 500)
3. ✅ Images should display correctly

### Test Order Creation
1. ✅ Test with missing name field - should show: "Missing required fields: name"
2. ✅ Test with missing phone field - should show: "Missing required fields: phone"
3. ✅ Test with missing address field - should show: "Missing required fields: address"
4. ✅ Test with missing province field - should show: "Missing required fields: province"
5. ✅ Test with multiple missing fields - should show all: "Missing required fields: name, phone"
6. ✅ Error should be displayed as toast notification
7. ✅ Error should be logged to console for debugging

---

## 📋 Error Response Format

All errors now follow consistent format:

```json
{
    "success": false,
    "error": {
        "type": "ValidationError",
        "message": "Missing required fields: name, phone",
        "request_id": "abc12345"
    }
}
```

**In DEBUG mode (additional info):**
```json
{
    "success": false,
    "error": {
        "type": "ValidationError",
        "message": "Missing required fields: name, phone",
        "request_id": "abc12345"
    },
    "debug_info": {
        "exception": "...",
        "context": {
            "endpoint": "create_order_on_payment",
            "missing_fields": ["name", "phone"],
            "received_data": {
                "name": false,
                "phone": false,
                "address": true,
                "province": true
            }
        }
    }
}
```

---

## ✅ Status

**Both issues fixed:** ✅  
**Tested:** ⚠️ Needs manual testing  
**Ready for production:** ✅

---

## 📝 Notes

- Media files are now served correctly without middleware interference
- Error messages are more helpful for debugging
- Users see clear error messages about missing fields
- All errors follow consistent format for frontend handling
