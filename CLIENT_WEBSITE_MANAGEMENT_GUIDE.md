# 🌟 Client Website Management Guide
## Everything You Need to Know as a Vibe Coder Managing a Client's Website

---

## 📋 Table of Contents

1. [Understanding Your Role](#understanding-your-role)
2. [Client Communication Guide](#client-communication-guide)
3. [How to Control/Manage the Website](#how-to-controlmanage-the-website)
4. [Making Changes & Adding Features](#making-changes--adding-features)
5. [Fixing Issues & Bugs](#fixing-issues--bugs)
6. [Website Maintenance](#website-maintenance)
7. [Database Management](#database-management)
8. [Backup & Security](#backup--security)
9. [Common Tasks & How-To's](#common-tasks--how-tos)
10. [What to Document for Your Client](#what-to-document-for-your-client)

---

## 🎯 Understanding Your Role

### What You're Responsible For:
✅ **Website functionality** - Making sure everything works  
✅ **Updates & new features** - When client requests changes  
✅ **Bug fixes** - Fixing problems that arise  
✅ **Maintenance** - Keeping the website updated and secure  
✅ **Database management** - Managing product data, orders, customers  
✅ **Backups** - Ensuring data is safe  

### What You're NOT Responsible For:
❌ **Content writing** - Client writes product descriptions  
❌ **Design decisions** - Client decides what looks good  
❌ **Marketing** - Client handles promotion  
❌ **24/7 support** - Set reasonable response times  

---

## 💬 Client Communication Guide

### Setting Expectations

**1. Response Time**
```
"Typically, I'll respond to messages within 24-48 hours during business days."
```

**2. Change Requests**
```
"Small changes (like updating text): 1-3 days
Medium changes (new features): 1-2 weeks
Large changes (major functionality): Discuss timeline first"
```

**3. Payment/Contract**
- Always agree on payment BEFORE starting work
- For ongoing maintenance: Monthly fee or hourly rate
- For new features: Quote first, then work

### Communication Best Practices

**✅ DO:**
- Ask clarifying questions if request is unclear
- Explain technical stuff in simple terms
- Confirm changes before starting
- Show progress/screenshots during development
- Document what was done

**❌ DON'T:**
- Start major changes without approval
- Make assumptions about what client wants
- Forget to backup before making changes
- Work without payment agreement
- Make changes live without testing

### Sample Communication Templates

**When Client Asks for New Feature:**
```
"Hi [Client Name],

I understand you'd like to add [feature]. 
To make sure I build exactly what you need, can you clarify:
- What should this feature do? (detailed description)
- Where should it appear on the website?
- Any specific design requirements?

Once I understand fully, I'll give you an estimate of time/cost.

Best,
[Your Name]"
```

**When Reporting an Issue:**
```
"Hi [Client Name],

I noticed [issue description]. 
This seems to be caused by [reason].

I can fix this by [solution]. 
It should take about [time estimate].

Should I proceed with the fix?

Best,
[Your Name]"
```

---

## 🎮 How to Control/Manage the Website

### 1. Admin Panel Access

**URL:** `https://yourwebsite.com/admin/`

**What You Can Do:**
- ✅ View/Edit Products
- ✅ Manage Orders
- ✅ View Customers
- ✅ Manage Promo Codes
- ✅ Update Hero Slides
- ✅ View Reports & Analytics

**Important:** Keep admin credentials SECURE. Never share with client unless they need access.

### 2. Server Access (If Deployed)

**If using a VPS/Cloud Server:**
```bash
# SSH into server
ssh username@your-server-ip

# Navigate to project
cd /path/to/your/project

# Common commands
python manage.py runserver  # Test locally
python manage.py migrate    # Update database
python manage.py collectstatic  # Update static files
```

### 3. Database Access

**SQLite (Development):**
- Database file: `db.sqlite3`
- Can view/edit with DB Browser for SQLite

**PostgreSQL (Production):**
- Usually managed through Django admin
- For direct access: Use pgAdmin or psql command line

---

## 🔧 Making Changes & Adding Features

### Step-by-Step Process

**1. Understand the Request**
- Ask clarifying questions
- Show examples/sketches if needed
- Confirm scope and timeline

**2. Plan the Changes**
- What files need to be modified?
- What database changes are needed?
- Any new dependencies?

**3. Test Locally First**
```bash
# Always test on your local machine first!
python manage.py runserver

# Test the new feature thoroughly
# Check for errors in console
# Test on different browsers if needed
```

**4. Create Backup**
```bash
# Backup database
python manage.py dumpdata > backup_before_changes.json

# Or copy db.sqlite3 file
cp db.sqlite3 db.sqlite3.backup
```

**5. Make Changes**
- Write/modify code
- Test again
- Fix any issues

**6. Deploy to Production**
```bash
# If using Git (recommended)
git add .
git commit -m "Add [feature name]"
git push origin main

# On server:
git pull origin main
python manage.py migrate  # If database changes
python manage.py collectstatic  # If static files changed
sudo systemctl restart gunicorn  # Restart server
```

**7. Verify on Live Site**
- Test the feature on live website
- Check for errors
- Confirm with client

### Common Change Scenarios

#### **Adding a New Product**
1. Go to Admin Panel → Products → Add Product
2. Fill in details (name, price, stock, image)
3. Save
4. ✅ Done! Product appears on homepage

#### **Changing Product Price**
1. Admin Panel → Products → Find product → Edit
2. Change price
3. Save
4. ✅ Price updated instantly

#### **Adding a Promo Code**
1. Admin Panel → Promo Codes → Add Promo Code
2. Enter code, discount, dates
3. Save
4. ✅ Customers can use it at checkout

#### **Changing Website Text/Content**
1. Find the template file (usually in `templates/`)
2. Edit the text
3. Save and push to server
4. ✅ Changes appear after deployment

---

## 🐛 Fixing Issues & Bugs

### Debugging Process

**1. Reproduce the Issue**
- Can you make it happen again?
- What steps cause the problem?
- What error message appears?

**2. Check Error Logs**
```bash
# Django logs (if deployed)
tail -f /var/log/django/error.log

# Or check terminal where server is running
# Look for red error messages
```

**3. Identify the Cause**
- Check code where error occurs
- Look at browser console (F12 → Console tab)
- Check database for missing data

**4. Fix the Issue**
- Make necessary code changes
- Test locally first
- Deploy fix

**5. Verify Fix**
- Test on live site
- Confirm with client that issue is resolved

### Common Issues & Solutions

#### **Issue: Website Shows Error 500**
**Cause:** Server error, usually code problem  
**Solution:**
```bash
# Check logs
# Look for specific error message
# Fix the code issue
# Restart server
```

#### **Issue: Product Not Appearing**
**Check:**
- Is product `is_active = True` in admin?
- Is stock > 0?
- Clear browser cache

#### **Issue: Orders Not Creating**
**Check:**
- Check browser console for errors
- Verify payment API is working
- Check database connection
- Look at server logs

#### **Issue: Images Not Loading**
**Check:**
- Image file exists in `media/` folder
- File permissions correct
- `MEDIA_URL` setting is correct
- Static files collected: `python manage.py collectstatic`

---

## 🔄 Website Maintenance

### Daily/Weekly Tasks

**✅ Check:**
- Website is loading correctly
- No error emails/alerts
- Orders are processing
- Payment system working

### Monthly Tasks

**✅ Review:**
- Error logs for recurring issues
- Server performance
- Database size (might need cleanup)
- Security updates

**✅ Updates:**
- Update Django if security patches available
- Update Python packages if needed
- Review and clean old order data (optional)

### Regular Maintenance Checklist

```markdown
[ ] Check website is accessible
[ ] Review error logs
[ ] Test order creation flow
[ ] Check payment processing
[ ] Verify backups are working
[ ] Update dependencies if needed
[ ] Review server performance
[ ] Clean up old data if necessary
```

---

## 🗄️ Database Management

### Important Database Concepts

**What's in Your Database:**
- Products (name, price, stock, images)
- Orders (customer info, items, totals, status)
- Customers (name, phone, address)
- Promo Codes (codes, discounts, dates)
- Hero Slides (banners on homepage)

### Common Database Tasks

#### **View All Orders**
```python
# In Django shell: python manage.py shell
from app.models import Order

orders = Order.objects.all()
for order in orders:
    print(f"{order.order_number} - {order.customer_name} - ${order.total}")
```

#### **Change Product Stock**
1. Admin Panel → Products → Select Product
2. Change stock number
3. Save

#### **Export Orders to CSV**
```python
# In Django shell
import csv
from app.models import Order

orders = Order.objects.all()
with open('orders.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Order Number', 'Customer', 'Total', 'Date'])
    for order in orders:
        writer.writerow([order.order_number, order.customer_name, order.total, order.created_at])
```

#### **Backup Database**
```bash
# SQLite
cp db.sqlite3 backup_$(date +%Y%m%d).sqlite3

# PostgreSQL
pg_dump database_name > backup_$(date +%Y%m%d).sql
```

#### **Restore Database**
```bash
# SQLite
cp backup_20231216.sqlite3 db.sqlite3

# PostgreSQL
psql database_name < backup_20231216.sql
```

---

## 💾 Backup & Security

### Backup Strategy

**What to Backup:**
1. ✅ Database (most important!)
2. ✅ Media files (product images, hero slides)
3. ✅ Code (in Git repository)
4. ✅ Environment variables (.env file)

**How Often:**
- Database: Daily (automated)
- Media files: Weekly
- Code: Every time you make changes (Git)

### Setting Up Automated Backups

**For SQLite (Simple):**
```bash
# Create backup script
#!/bin/bash
cp db.sqlite3 backups/backup_$(date +%Y%m%d_%H%M%S).sqlite3
# Keep only last 30 days
find backups/ -name "*.sqlite3" -mtime +30 -delete
```

**For PostgreSQL:**
```bash
# Use cron job
0 2 * * * pg_dump database_name > /backups/db_$(date +\%Y\%m\%d).sql
```

### Security Best Practices

**✅ DO:**
- Keep `DEBUG = False` in production
- Use strong `SECRET_KEY` (keep in .env, never commit)
- Keep dependencies updated
- Use HTTPS (SSL certificate)
- Regular backups
- Strong admin passwords

**❌ DON'T:**
- Commit `.env` file to Git
- Use `DEBUG = True` in production
- Share admin credentials
- Skip security updates
- Store passwords in code

---

## 📝 Common Tasks & How-To's

### Task: Add New Product
1. Admin Panel → Products → Add Product
2. Fill fields: Name, Price, Stock, Image, Description
3. Save
4. ✅ Product appears on homepage

### Task: Update Product Price
1. Admin Panel → Products → Find product → Edit
2. Change price
3. Save
4. ✅ Price updates immediately

### Task: View Orders
1. Admin Panel → Orders
2. See all orders with status
3. Click order to see details

### Task: Change Order Status
1. Admin Panel → Orders → Select Order
2. Change status dropdown
3. Save
4. ✅ Status updated

### Task: Add Promo Code
1. Admin Panel → Promo Codes → Add
2. Enter: Code, Discount %, Start/End Date
3. Save
4. ✅ Customers can use at checkout

### Task: Update Hero Slide (Homepage Banner)
1. Admin Panel → Hero Slides → Add/Edit
2. Upload image/video
3. Set order/position
4. Save
5. ✅ Appears on homepage

### Task: View Customer Information
1. Admin Panel → Customers
2. See all customers
3. Click to view details/order history

---

## 📚 What to Document for Your Client

### Create a Simple Guide for Your Client

**Document should include:**

1. **How to Access Admin Panel**
   - URL
   - Login credentials (secure delivery)
   - Screenshots of main pages

2. **How to Add/Edit Products**
   - Step-by-step with screenshots
   - What each field means
   - Image size recommendations

3. **How to View Orders**
   - Where to find orders
   - How to understand order details
   - How to update order status

4. **How to Use Promo Codes**
   - Creating codes
   - Setting discounts
   - When codes expire

5. **Contact Information**
   - How to reach you for support
   - Response time expectations
   - What to include when reporting issues

### Sample Client Documentation

Create a file: `CLIENT_USER_GUIDE.md`

```markdown
# Website Admin Guide for [Client Name]

## Accessing Admin Panel
URL: https://yourwebsite.com/admin/
Username: [username]
Password: [password - share securely!]

## Adding a Product
1. Click "Products" in admin panel
2. Click "Add Product"
3. Fill in:
   - Product Name
   - Price
   - Stock Quantity
   - Upload Image (recommended: 800x800px)
   - Description (optional)
4. Click "Save"
5. Product appears on homepage immediately

## Viewing Orders
1. Click "Orders" in admin panel
2. See list of all orders
3. Click order number to see details
4. Update status as needed

## Need Help?
Contact: [your email]
Response time: Within 24-48 hours
```

---

## 🎓 Skills You Should Learn

### Essential Skills (Must Know)
- ✅ Basic Git (commit, push, pull)
- ✅ Reading error messages
- ✅ Using Django admin panel
- ✅ Basic terminal/command line
- ✅ Understanding file structure

### Helpful Skills (Good to Learn)
- 📚 Debugging techniques
- 📚 Database queries (basic)
- 📚 Server management basics
- 📚 Testing your code
- 📚 Reading documentation

### Learning Resources
- Django Official Docs: https://docs.djangoproject.com/
- Stack Overflow: For specific questions
- YouTube: Django tutorials
- GitHub: See other Django projects

---

## 💡 Pro Tips

1. **Always Test Locally First**
   - Never make changes directly on live site
   - Test thoroughly before deploying

2. **Use Git for Everything**
   - Commit often
   - Write clear commit messages
   - Push to GitHub regularly

3. **Keep Documentation Updated**
   - Document what you build
   - Note any special configurations
   - Keep client guide current

4. **Set Boundaries**
   - Agree on scope before starting
   - Charge for extra work
   - Set reasonable timelines

5. **Learn to Say No**
   - Don't promise things you can't deliver
   - Be honest about complexity
   - Suggest alternatives when needed

---

## 🆘 When You Need Help

### Where to Get Help:

1. **Error Messages**
   - Copy the full error
   - Google the error message
   - Check Stack Overflow

2. **Django Documentation**
   - Official docs are great
   - Search for specific features
   - Check examples

3. **Ask Questions**
   - Be specific about the problem
   - Include error messages
   - Show relevant code

4. **Take Breaks**
   - Sometimes stepping away helps
   - Fresh eyes see things differently

---

## 📋 Quick Reference

### Essential Commands
```bash
# Run development server
python manage.py runserver

# Update database
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Backup database (SQLite)
cp db.sqlite3 backup.sqlite3
```

### Important Files
- `settings.py` - Website configuration
- `models.py` - Database structure
- `views.py` - Website logic
- `urls.py` - URL routing
- `admin.py` - Admin panel setup
- `.env` - Secret keys (NEVER commit!)

---

## 🎯 Final Checklist Before Going Live

- [ ] Website tested thoroughly
- [ ] All features working
- [ ] Admin panel accessible
- [ ] Backups configured
- [ ] Security settings correct (DEBUG=False)
- [ ] SSL certificate installed (HTTPS)
- [ ] Client documentation created
- [ ] Support process established
- [ ] Payment system tested
- [ ] Database backed up

---

## 📞 Remember

**You Got This!** 🌟

- Start small, learn as you go
- Test everything before deploying
- Keep backups
- Communicate clearly with client
- Don't be afraid to ask for help
- Take breaks when stuck
- Document what you do

**Being a "vibe coder" means:**
- Learning and growing
- Making mistakes (that's okay!)
- Building cool things
- Helping clients succeed

---

**Good luck! You're doing great! 🚀**

---

*Last Updated: 2025-12-16*  
*For questions or improvements to this guide, update it as you learn!*
