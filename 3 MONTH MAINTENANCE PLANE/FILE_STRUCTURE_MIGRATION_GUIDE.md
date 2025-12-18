# 📁 File Structure Migration Guide

Your templates and static files have been reorganized for better maintainability! This guide shows you what needs to be updated.

## ✅ What Was Done

### Templates Reorganized:
```
Before:                              After:
app/index.html                  →    app/shop/index.html
app/checkout.html               →    app/shop/checkout.html
app/order_success.html          →    app/shop/order_success.html
app/employee_dashboard.html     →    app/employee/dashboard.html
app/employee_order_detail.html  →    app/employee/order_detail.html
app/employee_order_card.html    →    app/employee/components/order_card.html
app/employee_order_card_kanban.html → app/employee/components/order_card_kanban.html
app/cod_confirmation.html       →    app/cod/confirmation.html
app/cod_print.html              →    app/cod/print.html
app/about_us.html               →    app/pages/about_us.html
app/contact.html                →    app/pages/contact.html
app/privacy_policy.html         →    app/pages/privacy_policy.html
app/shipping_policy.html        →    app/pages/shipping_policy.html
```

### Static Files Reorganized:
```
Before:                              After:
css/index.css                   →    shop/css/index.css
css/checkout.css                →    shop/css/checkout.css
css/order_success.css           →    shop/css/order_success.css
css/cod_confirmation.css        →    cod/css/cod_confirmation.css
js/index.js                     →    shop/js/index.js
js/checkout.js                  →    shop/js/checkout.js
js/order_success.js             →    shop/js/order_success.js
js/cod_confirmation.js          →    cod/js/cod_confirmation.js
js/qrcode.min.js                →    common/js/qrcode.min.js
js/html5-qrcode.min.js          →    common/js/html5-qrcode.min.js
images/madam-da-logo.png        →    common/images/logos/madam-da-logo.png
images/bakong-logo.svg          →    common/images/logos/bakong-logo.svg
images/jandt-logo.png           →    common/images/logos/jandt-logo.png
images/favicon.png              →    common/images/favicon.png
```

## 🔧 Required Code Updates

### 1. Update `app/views.py`

Search and replace template paths:

```python
# OLD CODE:
def shop_view(request):
    return render(request, 'app/index.html', context)

def checkout_view(request):
    return render(request, 'app/checkout.html', context)

def order_success_view(request):
    return render(request, 'app/order_success.html', context)

def cod_confirmation_view(request, order_number=None):
    return render(request, 'app/cod_confirmation.html', context)

def cod_print_view(request, order_number):
    return render(request, 'app/cod_print.html', context)

def about_us_view(request):
    return render(request, 'app/about_us.html')

def contact_view(request):
    return render(request, 'app/contact.html')

def privacy_policy_view(request):
    return render(request, 'app/privacy_policy.html')

def shipping_policy_view(request):
    return render(request, 'app/shipping_policy.html')
```

```python
# NEW CODE:
def shop_view(request):
    return render(request, 'app/shop/index.html', context)

def checkout_view(request):
    return render(request, 'app/shop/checkout.html', context)

def order_success_view(request):
    return render(request, 'app/shop/order_success.html', context)

def cod_confirmation_view(request, order_number=None):
    return render(request, 'app/cod/confirmation.html', context)

def cod_print_view(request, order_number):
    return render(request, 'app/cod/print.html', context)

def about_us_view(request):
    return render(request, 'app/pages/about_us.html')

def contact_view(request):
    return render(request, 'app/pages/contact.html')

def privacy_policy_view(request):
    return render(request, 'app/pages/privacy_policy.html')

def shipping_policy_view(request):
    return render(request, 'app/pages/shipping_policy.html')
```

### 2. Update `app/employee_views.py`

```python
# OLD CODE:
def employee_dashboard(request):
    return render(request, 'app/employee_dashboard.html', context)

def employee_order_detail(request, order_number):
    return render(request, 'app/employee_order_detail.html', context)

def employee_print_qr(request, order_number):
    return render(request, 'app/cod_print.html', context)
```

```python
# NEW CODE:
def employee_dashboard(request):
    return render(request, 'app/employee/dashboard.html', context)

def employee_order_detail(request, order_number):
    return render(request, 'app/employee/order_detail.html', context)

def employee_print_qr(request, order_number):
    return render(request, 'app/cod/print.html', context)
```

### 3. Update Template Includes

In `app/employee/dashboard.html`:

```django
<!-- OLD -->
{% include 'app/employee_order_card_kanban.html' with order=order show_items=True %}

<!-- NEW -->
{% include 'app/employee/components/order_card_kanban.html' with order=order show_items=True %}
```

### 4. Update Static File References

In all templates, update CSS references:

```django
<!-- OLD -->
<link rel="stylesheet" href="{% static 'css/index.css' %}">
<link rel="stylesheet" href="{% static 'css/checkout.css' %}">
<link rel="stylesheet" href="{% static 'css/order_success.css' %}">
<link rel="stylesheet" href="{% static 'css/cod_confirmation.css' %}">

<!-- NEW -->
<link rel="stylesheet" href="{% static 'shop/css/index.css' %}">
<link rel="stylesheet" href="{% static 'shop/css/checkout.css' %}">
<link rel="stylesheet" href="{% static 'shop/css/order_success.css' %}">
<link rel="stylesheet" href="{% static 'cod/css/cod_confirmation.css' %}">
```

Update JavaScript references:

```django
<!-- OLD -->
<script src="{% static 'js/index.js' %}"></script>
<script src="{% static 'js/checkout.js' %}"></script>
<script src="{% static 'js/order_success.js' %}"></script>
<script src="{% static 'js/cod_confirmation.js' %}"></script>
<script src="{% static 'js/qrcode.min.js' %}"></script>
<script src="{% static 'js/html5-qrcode.min.js' %}"></script>

<!-- NEW -->
<script src="{% static 'shop/js/index.js' %}"></script>
<script src="{% static 'shop/js/checkout.js' %}"></script>
<script src="{% static 'shop/js/order_success.js' %}"></script>
<script src="{% static 'cod/js/cod_confirmation.js' %}"></script>
<script src="{% static 'common/js/qrcode.min.js' %}"></script>
<script src="{% static 'common/js/html5-qrcode.min.js' %}"></script>
```

Update image references:

```django
<!-- OLD -->
<img src="{% static 'images/madam-da-logo.png' %}" alt="Madam Da">
<img src="{% static 'images/bakong-logo.svg' %}" alt="Bakong">
<img src="{% static 'images/jandt-logo.png' %}" alt="J&T Express">
<link rel="icon" href="{% static 'images/favicon.png' %}">

<!-- NEW -->
<img src="{% static 'common/images/logos/madam-da-logo.png' %}" alt="Madam Da">
<img src="{% static 'common/images/logos/bakong-logo.svg' %}" alt="Bakong">
<img src="{% static 'common/images/logos/jandt-logo.png' %}" alt="J&T Express">
<link rel="icon" href="{% static 'common/images/favicon.png' %}">
```

## 🔍 How to Find & Replace

### VS Code / Cursor:
1. Press `Ctrl+Shift+F` (Windows) or `Cmd+Shift+F` (Mac)
2. Search for: `'app/employee_dashboard.html'`
3. Replace with: `'app/employee/dashboard.html'`
4. Click "Replace All"

### Using Find & Replace for All Files:

**For Templates:**
```
Find:     'app/index.html'
Replace:  'app/shop/index.html'

Find:     'app/checkout.html'
Replace:  'app/shop/checkout.html'

Find:     'app/employee_dashboard.html'
Replace:  'app/employee/dashboard.html'

Find:     'app/employee_order_card_kanban.html'
Replace:  'app/employee/components/order_card_kanban.html'

Find:     'app/cod_confirmation.html'
Replace:  'app/cod/confirmation.html'

Find:     'app/cod_print.html'
Replace:  'app/cod/print.html'
```

**For Static Files:**
```
Find:     {% static 'css/index.css' %}
Replace:  {% static 'shop/css/index.css' %}

Find:     {% static 'js/index.js' %}
Replace:  {% static 'shop/js/index.js' %}

Find:     {% static 'images/madam-da-logo.png' %}
Replace:  {% static 'common/images/logos/madam-da-logo.png' %}

Find:     {% static 'js/qrcode.min.js' %}
Replace:  {% static 'common/js/qrcode.min.js' %}
```

## ✅ Checklist

After making changes, verify:

- [ ] `app/views.py` - All render() paths updated
- [ ] `app/employee_views.py` - All render() paths updated
- [ ] Template files - All {% include %} paths updated
- [ ] Template files - All {% static 'css/...' %} paths updated
- [ ] Template files - All {% static 'js/...' %} paths updated
- [ ] Template files - All {% static 'images/...' %} paths updated
- [ ] Run `python manage.py collectstatic` if in production
- [ ] Test all pages to ensure they load correctly
- [ ] Check browser console for 404 errors

## 🧪 Testing

Test each page after updating:

1. **Shop Pages:**
   - Visit `/` (shop page)
   - Visit `/checkout/`
   - Place an order and visit `/order/success/`

2. **Employee Pages:**
   - Visit `/employee/` (dashboard)
   - Click on an order to view detail

3. **COD Pages:**
   - Visit a COD confirmation page
   - Try printing a QR code

4. **Static Pages:**
   - Visit `/about-us/`
   - Visit `/contact/`
   - Visit `/privacy-policy/`
   - Visit `/shipping-policy/`

## 🚨 Common Issues

### Issue: 404 Template Not Found
**Solution:** Check that you updated the render() path in views.py

### Issue: CSS/JS Not Loading
**Solution:** 
1. Check static file paths in templates
2. Run `python manage.py collectstatic` if needed
3. Clear browser cache (Ctrl+Shift+R)

### Issue: Images Not Displaying
**Solution:** Update image paths to use new `common/images/` structure

## 📚 Additional Resources

- See `templates/app/README.md` for template structure details
- See `static/README.md` for static files structure details

---

**Created:** December 2025
**Status:** ⚠️ Requires Manual Code Updates
**Priority:** HIGH - Update before next deployment

