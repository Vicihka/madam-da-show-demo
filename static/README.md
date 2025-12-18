# 📁 Static Assets Structure Guide

This folder contains all CSS, JavaScript, and images organized by functionality.

## 📂 Folder Structure

```
static/
├── shop/              # Customer shopping assets
│   ├── css/
│   │   ├── index.css           → Main shop page styles
│   │   ├── checkout.css        → Checkout page styles
│   │   └── order_success.css   → Order success styles
│   └── js/
│       ├── index.js            → Shop page functionality
│       ├── checkout.js         → Checkout page logic
│       └── order_success.js    → Order success functionality
│
├── employee/          # Employee dashboard assets
│   ├── css/
│   │   └── dashboard.css       → Employee dashboard styles (future)
│   └── js/
│       └── dashboard.js        → Dashboard functionality (future)
│
├── cod/               # COD-specific assets
│   ├── css/
│   │   └── cod_confirmation.css → COD confirmation page styles
│   └── js/
│       └── cod_confirmation.js  → COD confirmation logic
│
└── common/            # Shared/global assets
    ├── css/
    │   └── global.css          → Global styles (future)
    ├── js/
    │   ├── qrcode.min.js       → QR code generation library
    │   └── html5-qrcode.min.js → QR code scanning library
    └── images/
        ├── favicon.png         → Site favicon
        └── logos/
            ├── bakong-logo.svg     → Bakong payment logo
            ├── jandt-logo.png      → J&T Express logo
            └── madam-da-logo.png   → Madam Da company logo
```

## 🎯 Usage in Templates

### Loading CSS Files

```django
{% load static %}

<!-- Shop pages -->
<link rel="stylesheet" href="{% static 'shop/css/index.css' %}">
<link rel="stylesheet" href="{% static 'shop/css/checkout.css' %}">

<!-- Employee pages -->
<link rel="stylesheet" href="{% static 'employee/css/dashboard.css' %}">

<!-- COD pages -->
<link rel="stylesheet" href="{% static 'cod/css/cod_confirmation.css' %}">

<!-- Common styles (if needed) -->
<link rel="stylesheet" href="{% static 'common/css/global.css' %}">
```

### Loading JavaScript Files

```django
<!-- Shop functionality -->
<script src="{% static 'shop/js/index.js' %}"></script>
<script src="{% static 'shop/js/checkout.js' %}"></script>

<!-- COD functionality -->
<script src="{% static 'cod/js/cod_confirmation.js' %}"></script>

<!-- Common libraries -->
<script src="{% static 'common/js/qrcode.min.js' %}"></script>
<script src="{% static 'common/js/html5-qrcode.min.js' %}"></script>
```

### Using Images

```django
<!-- Logos -->
<img src="{% static 'common/images/logos/madam-da-logo.png' %}" alt="Madam Da">
<img src="{% static 'common/images/logos/bakong-logo.svg' %}" alt="Bakong">
<img src="{% static 'common/images/logos/jandt-logo.png' %}" alt="J&T Express">

<!-- Favicon -->
<link rel="icon" href="{% static 'common/images/favicon.png' %}">
```

## 🔄 Path Migration Guide

| Old Path | New Path |
|----------|----------|
| `css/index.css` | `shop/css/index.css` |
| `css/checkout.css` | `shop/css/checkout.css` |
| `css/order_success.css` | `shop/css/order_success.css` |
| `css/cod_confirmation.css` | `cod/css/cod_confirmation.css` |
| `js/index.js` | `shop/js/index.js` |
| `js/checkout.js` | `shop/js/checkout.js` |
| `js/order_success.js` | `shop/js/order_success.js` |
| `js/cod_confirmation.js` | `cod/js/cod_confirmation.js` |
| `js/qrcode.min.js` | `common/js/qrcode.min.js` |
| `js/html5-qrcode.min.js` | `common/js/html5-qrcode.min.js` |
| `images/madam-da-logo.png` | `common/images/logos/madam-da-logo.png` |
| `images/bakong-logo.svg` | `common/images/logos/bakong-logo.svg` |
| `images/jandt-logo.png` | `common/images/logos/jandt-logo.png` |
| `images/favicon.png` | `common/images/favicon.png` |

## 📝 File Naming Conventions

### CSS Files
- Use descriptive names matching the page: `dashboard.css`, `checkout.css`
- Put page-specific styles in the appropriate folder
- Use `common/css/` for styles shared across multiple pages

### JavaScript Files
- Match the page name: `dashboard.js`, `checkout.js`
- External libraries go in `common/js/`
- Keep page-specific logic in the appropriate folder

### Images
- Logos go in `common/images/logos/`
- Icons and general images go in `common/images/`
- Page-specific images can go in their respective folders (e.g., `shop/images/`)

## 🎨 Benefits of This Structure

1. **Easy to Find**: Know exactly where to look for files
2. **Organized by Feature**: Shop files together, employee files together
3. **Clear Ownership**: Each section has its own assets
4. **Scalable**: Easy to add new sections without cluttering
5. **Maintainable**: Changes to one section don't affect others

## 🔍 Quick Reference

- **Shopping page styles?** → `shop/css/`
- **Employee dashboard styles?** → `employee/css/`
- **COD related styles?** → `cod/css/`
- **Shared libraries?** → `common/js/`
- **Company logos?** → `common/images/logos/`

## 🚀 Adding New Assets

### For a new feature section:
1. Create folder: `static/feature_name/`
2. Add subfolders: `css/`, `js/`, `images/` (as needed)
3. Update this README

### For shared assets:
1. Put in `common/css/`, `common/js/`, or `common/images/`
2. Document the purpose clearly

## ⚡ Performance Tips

- Minify CSS/JS files before production
- Compress images in `common/images/`
- Use CDN for common libraries when possible
- Lazy load images where appropriate

---

**Last Updated:** December 2025
**Structure Version:** 2.0

