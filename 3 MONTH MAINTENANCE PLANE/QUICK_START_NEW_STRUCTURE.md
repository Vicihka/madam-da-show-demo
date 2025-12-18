# ⚡ Quick Start: New File Structure

## 🎯 What Happened?

Your files are now organized! Instead of everything mixed together, files are grouped by what they do.

## 📁 New Folders

| Folder | What's Inside | When to Use |
|--------|---------------|-------------|
| `shop/` | Customer shopping pages | Editing main shop, checkout, order success |
| `employee/` | Employee dashboard | Working on order management dashboard |
| `cod/` | Cash on Delivery pages | COD confirmation, QR codes |
| `pages/` | Info pages | About, Contact, Privacy, Shipping |
| `common/` | Shared assets | Logos, libraries used everywhere |

## 🔧 What You Need to Do

### 1. Update Your Django Views (REQUIRED)

Open these files and update the paths:

**File: `app/views.py`**
- Change: `'app/index.html'` → `'app/shop/index.html'`
- Change: `'app/checkout.html'` → `'app/shop/checkout.html'`
- Change: `'app/order_success.html'` → `'app/shop/order_success.html'`
- Change: `'app/cod_confirmation.html'` → `'app/cod/confirmation.html'`
- Change: `'app/cod_print.html'` → `'app/cod/print.html'`
- Change: `'app/about_us.html'` → `'app/pages/about_us.html'`
- Change: `'app/contact.html'` → `'app/pages/contact.html'`
- Change: `'app/privacy_policy.html'` → `'app/pages/privacy_policy.html'`
- Change: `'app/shipping_policy.html'` → `'app/pages/shipping_policy.html'`

**File: `app/employee_views.py`**
- Change: `'app/employee_dashboard.html'` → `'app/employee/dashboard.html'`
- Change: `'app/employee_order_detail.html'` → `'app/employee/order_detail.html'`

### 2. Update Template Includes

**File: `templates/app/employee/dashboard.html`**

Find this line:
```django
{% include 'app/employee_order_card_kanban.html' with order=order show_items=True %}
```

Change to:
```django
{% include 'app/employee/components/order_card_kanban.html' with order=order show_items=True %}
```

### 3. Update Static File Paths in Templates

In all template files, update:

**CSS:**
```django
<!-- Change from: -->
<link rel="stylesheet" href="{% static 'css/index.css' %}">
<!-- Change to: -->
<link rel="stylesheet" href="{% static 'shop/css/index.css' %}">
```

**JavaScript:**
```django
<!-- Change from: -->
<script src="{% static 'js/index.js' %}"></script>
<!-- Change to: -->
<script src="{% static 'shop/js/index.js' %}"></script>
```

**Images/Logos:**
```django
<!-- Change from: -->
<img src="{% static 'images/madam-da-logo.png' %}">
<!-- Change to: -->
<img src="{% static 'common/images/logos/madam-da-logo.png' %}">
```

**Common Libraries:**
```django
<!-- Change from: -->
<script src="{% static 'js/qrcode.min.js' %}"></script>
<!-- Change to: -->
<script src="{% static 'common/js/qrcode.min.js' %}"></script>
```

## ✅ Quick Testing Checklist

After making changes, test these pages:

- [ ] `/` - Shop page loads with styles
- [ ] `/checkout/` - Checkout works
- [ ] `/employee/` - Dashboard loads (NEW KANBAN DESIGN!)
- [ ] `/about-us/` - About page works
- [ ] `/contact/` - Contact page works
- [ ] COD confirmation page
- [ ] Print QR code page

## 🔍 Fast Find & Replace

Use your editor's find & replace (Ctrl+Shift+F):

### In Python Files (views.py, employee_views.py):
```
Find:    'app/index.html'
Replace: 'app/shop/index.html'

Find:    'app/employee_dashboard.html'
Replace: 'app/employee/dashboard.html'
```

### In Template Files:
```
Find:    'app/employee_order_card_kanban.html'
Replace: 'app/employee/components/order_card_kanban.html'

Find:    {% static 'css/
Replace: {% static 'shop/css/

Find:    {% static 'js/
Replace: {% static 'shop/js/

Find:    {% static 'images/
Replace: {% static 'common/images/
```

## 🚨 Common Mistakes to Avoid

1. ❌ Forgetting to update views.py → Pages will show 404
2. ❌ Not updating {% include %} paths → Components won't load
3. ❌ Missing {% static %} updates → CSS/JS won't load
4. ❌ Not clearing browser cache → Old files cached

## 💡 Pro Tips

1. **Use Global Search:** Search entire project for old paths
2. **Test Immediately:** Test each page after updating
3. **Check Console:** Browser console shows 404 errors for missing files
4. **Commit Often:** Git commit after each successful section

## 📚 Full Documentation

For complete details, see:
- `FILE_STRUCTURE_MIGRATION_GUIDE.md` - Complete migration instructions
- `NEW_FOLDER_STRUCTURE.md` - Visual folder structure
- `templates/app/README.md` - Template organization details
- `static/README.md` - Static files organization details

## ⏱️ Time Estimate

- Views updates: ~5 minutes
- Template includes: ~2 minutes
- Static paths: ~10 minutes
- Testing: ~10 minutes
- **Total: ~30 minutes**

## 🎉 Benefits You'll Get

- ✅ **Easy to Find Files:** Know exactly where everything is
- ✅ **Better Organization:** Related files grouped together
- ✅ **Faster Development:** No more hunting for files
- ✅ **Team-Friendly:** New developers understand structure
- ✅ **Scalable:** Easy to add new features
- ✅ **Industry Standard:** Professional folder structure

---

**Ready?** Start with updating `app/views.py` and `app/employee_views.py` first!

🚀 **Good luck!** You got this!

