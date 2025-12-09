# 💰 Website Cost Calculation for Clients

## 📊 **Pricing Formula**

The total cost a client pays is calculated using this formula:

```
TOTAL = SUBTOTAL + SHIPPING FEE - DISCOUNT
```

---

## 🔢 **Detailed Breakdown**

### **1. Subtotal** 
**How it's calculated:**
```
Subtotal = Sum of (Product Price × Quantity) for all items in cart
```

**Example:**
- Product A: $10.00 × 2 = $20.00
- Product B: $15.00 × 1 = $15.00
- Product C: $5.00 × 3 = $15.00
- **Subtotal = $50.00**

---

### **2. Shipping Fee**
**Current Setting:**
```
Shipping Fee = $0.00 (FREE SHIPPING)
```

**Note:** The website shows "Delivery fee: ~~$1.50~~ $0" (free shipping)

---

### **3. Discount Amount**
**How it's calculated:**
- If customer applies a **promo code**, discount is calculated based on promo code rules:
  - **Percentage discount:** `Discount = (Subtotal × Discount %) / 100`
  - **Fixed amount discount:** `Discount = Fixed Amount`
- If no promo code: `Discount = $0.00`

**Example:**
- Subtotal: $50.00
- Promo code: "SAVE10" (10% off)
- **Discount = $50.00 × 10% = $5.00**

---

### **4. Total (Final Cost)**
**Formula:**
```
Total = Subtotal + Shipping Fee - Discount Amount
```

**Example Calculation:**
```
Subtotal:        $50.00
Shipping Fee:    $0.00
Discount:        -$5.00
─────────────────────────
TOTAL:           $45.00
```

---

## 📝 **Real Example**

**Customer Order:**
- 2x Product A @ $10.00 each = $20.00
- 1x Product B @ $15.00 each = $15.00
- 3x Product C @ $5.00 each = $15.00

**Calculation:**
```
Subtotal:        $50.00
Shipping Fee:    $0.00  (FREE)
Discount:        $0.00  (No promo code)
─────────────────────────
TOTAL:           $50.00
```

**With Promo Code (10% off):**
```
Subtotal:        $50.00
Shipping Fee:    $0.00  (FREE)
Discount:        -$5.00 (10% off)
─────────────────────────
TOTAL:           $45.00
```

---

## 🎯 **Key Points**

1. **Free Shipping:** All orders have $0.00 shipping fee
2. **No Hidden Fees:** The total shown is exactly what the customer pays
3. **Discounts Applied:** Promo codes reduce the final total
4. **Payment Methods:** Same price for all payment methods:
   - KHQR
   - ACLEDA Bank
   - Wing Money
   - Cash on Delivery (COD)

---

## 💻 **Where This is Calculated**

**Frontend (JavaScript):**
- File: `templates/app/checkout.html`
- Lines: ~1993-1997
- Code:
```javascript
const subtotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
const deliveryFee = 0;
const discountAmount = window.promoDiscount || 0;
const total = Math.round(Math.max(0, subtotal + deliveryFee - discountAmount) * 100) / 100;
```

**Backend (Python/Django):**
- File: `app/views.py`
- Function: `create_order_on_payment()`
- Lines: ~759-799
- Stores: `subtotal`, `shipping_fee`, `discount_amount`, `total` in database

---

## 📱 **What Customer Sees**

On the checkout page, customers see:
```
Order Summary:
─────────────────────────
Product A x 2        $20.00
Product B x 1        $15.00
Product C x 3        $15.00
─────────────────────────
Delivery fee         $0.00
Discount            -$5.00
─────────────────────────
TOTAL                $45.00
```

---

## ✅ **Summary**

**Simple Formula:**
```
Client Pays = (Sum of all products) - (Promo discount)
```

**Current Settings:**
- ✅ Free shipping ($0.00)
- ✅ Promo codes supported
- ✅ No additional fees
- ✅ Transparent pricing

---

*Last Updated: Based on current codebase analysis*

