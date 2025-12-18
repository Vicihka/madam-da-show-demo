# 📁 Templates Structure Guide

This folder contains all HTML templates organized by functionality.

## 📂 Folder Structure

```
app/
├── shop/              # Customer-facing shopping pages
│   ├── index.html              → Main shop/product listing page
│   ├── checkout.html           → Checkout page
│   └── order_success.html      → Order confirmation page
│
├── employee/          # Employee dashboard & management
│   ├── dashboard.html          → Main Kanban employee dashboard
│   ├── order_detail.html       → Detailed view of single order
│   └── components/
│       ├── order_card.html        → Reusable order card (list view)
│       └── order_card_kanban.html → Reusable order card (Kanban view)
│
├── cod/               # Cash on Delivery related pages
│   ├── confirmation.html       → Customer COD confirmation page
│   └── print.html              → Printable QR code page for COD orders
│
└── pages/             # Static informational pages
    ├── about_us.html           → About us page
    ├── contact.html            → Contact page
    ├── privacy_policy.html     → Privacy policy
    └── shipping_policy.html    → Shipping policy
```

## 🎯 Quick Reference

### Customer Journey:
1. `shop/index.html` - Browse products
2. `shop/checkout.html` - Place order
3. `shop/order_success.html` - View confirmation
4. `cod/confirmation.html` - Confirm receipt (COD only)

### Employee Workflow:
1. `employee/dashboard.html` - View all orders
2. `employee/order_detail.html` - View single order details
3. `cod/print.html` - Print QR for COD orders

### Information Pages:
- `pages/about_us.html`
- `pages/contact.html`
- `pages/privacy_policy.html`
- `pages/shipping_policy.html`

## 🔧 Usage in Views

When rendering templates in your Django views, use the new paths:

```python
# Old way:
return render(request, 'app/employee_dashboard.html')

# New way:
return render(request, 'app/employee/dashboard.html')
```

### Path Migration Guide:

| Old Path | New Path |
|----------|----------|
| `app/index.html` | `app/shop/index.html` |
| `app/checkout.html` | `app/shop/checkout.html` |
| `app/order_success.html` | `app/shop/order_success.html` |
| `app/employee_dashboard.html` | `app/employee/dashboard.html` |
| `app/employee_order_detail.html` | `app/employee/order_detail.html` |
| `app/employee_order_card.html` | `app/employee/components/order_card.html` |
| `app/employee_order_card_kanban.html` | `app/employee/components/order_card_kanban.html` |
| `app/cod_confirmation.html` | `app/cod/confirmation.html` |
| `app/cod_print.html` | `app/cod/print.html` |
| `app/about_us.html` | `app/pages/about_us.html` |
| `app/contact.html` | `app/pages/contact.html` |
| `app/privacy_policy.html` | `app/pages/privacy_policy.html` |
| `app/shipping_policy.html` | `app/pages/shipping_policy.html` |

## 📝 Notes

- **Components** are reusable template parts (like order cards)
- Include components using: `{% include 'app/employee/components/order_card.html' %}`
- All paths are relative to the `templates/` directory
- Keep related files together for easier maintenance

## 🔍 Finding Files

- **Shopping features?** → Look in `shop/`
- **Employee features?** → Look in `employee/`
- **COD features?** → Look in `cod/`
- **Info pages?** → Look in `pages/`

---

**Last Updated:** December 2025
**Structure Version:** 2.0

