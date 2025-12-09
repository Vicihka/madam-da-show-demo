# 📦 Migrate Data from SQLite to PostgreSQL

## ✅ **Keep Your Superuser & All Data**

This guide will help you migrate all your existing data (including your superuser) from SQLite to PostgreSQL.

---

## 🚀 **Easy Way: Use the Script**

### **Step 1: Create PostgreSQL Database**

**Using pgAdmin:**
1. Open pgAdmin
2. Right-click **Databases** → **Create** → **Database**
3. Name: `madamda_db`
4. Click **Save**

**OR using Command Line:**
```sql
psql -U postgres
CREATE DATABASE madamda_db;
\q
```

### **Step 2: Run Migration Script**

Double-click: `MIGRATE_TO_POSTGRESQL.bat`

The script will:
1. ✅ Export all data from SQLite
2. ✅ Switch to PostgreSQL
3. ✅ Run migrations
4. ✅ Import all your data
5. ✅ Preserve your superuser account

**Enter your PostgreSQL details when asked:**
- Database: `madamda_db`
- User: `postgres`
- Password: Your PostgreSQL password
- Host: `localhost`
- Port: `5432`

---

## 📋 **Manual Migration (Step by Step)**

### **Step 1: Export Data from SQLite**

```bash
# Activate venv
venv\Scripts\activate

# Export all data
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > data_export.json
```

### **Step 2: Set PostgreSQL Environment Variables**

**Windows PowerShell:**
```powershell
$env:DB_NAME="madamda_db"
$env:DB_USER="postgres"
$env:DB_PASSWORD="your_password"
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
```

**Windows CMD:**
```cmd
set DB_NAME=madamda_db
set DB_USER=postgres
set DB_PASSWORD=your_password
set DB_HOST=localhost
set DB_PORT=5432
```

### **Step 3: Run Migrations on PostgreSQL**

```bash
python manage.py makemigrations
python manage.py migrate
```

### **Step 4: Import Data to PostgreSQL**

```bash
python manage.py loaddata data_export.json
```

### **Step 5: Clean Up**

```bash
del data_export.json
```

---

## ✅ **What Gets Migrated**

- ✅ **Superuser accounts** (your admin login)
- ✅ **All orders** (customer orders)
- ✅ **All products** (your products)
- ✅ **Customers** (customer data)
- ✅ **Promo codes** (promotion codes)
- ✅ **Promoters** (promoter data)
- ✅ **Everything else** (all your data)

---

## 🎯 **After Migration**

1. **Start server:**
   ```bash
   START_SERVER_WEBSOCKET.bat
   ```

2. **Login to admin:**
   ```
   http://127.0.0.1:8000/admin/
   ```
   Use your **existing superuser** credentials!

3. **Verify data:**
   - Check orders are there
   - Check products are there
   - Everything should be the same!

---

## ⚠️ **Important Notes**

### **Before Migration:**
- ✅ Make sure PostgreSQL is running
- ✅ Create the database first
- ✅ Backup SQLite database (optional but recommended)

### **During Migration:**
- ✅ Don't close the terminal
- ✅ Wait for all steps to complete
- ✅ If errors occur, check the messages

### **After Migration:**
- ✅ Your SQLite database (`db.sqlite3`) is still there (backup)
- ✅ All data is now in PostgreSQL
- ✅ You can delete SQLite file later if you want

---

## 🔍 **Verify Migration**

### **Check Your Data:**

1. **Login to admin panel**
2. **Check Orders** - Should see all your orders
3. **Check Products** - Should see all products
4. **Check Customers** - Should see all customers
5. **Everything should be there!**

---

## 🎉 **Benefits**

### **After Migration:**
- ✅ **Better performance** - PostgreSQL is faster
- ✅ **More reliable** - Better for production
- ✅ **Scalable** - Can handle many users
- ✅ **All your data preserved** - Nothing lost!

---

## 📝 **Quick Summary**

1. **Create PostgreSQL database:** `madamda_db`
2. **Run:** `MIGRATE_TO_POSTGRESQL.bat`
3. **Enter PostgreSQL details**
4. **Wait for migration to complete**
5. **Done!** Your superuser and all data are preserved!

---

## ✅ **Ready to Migrate!**

Your superuser and all data will be preserved! 🚀

Just run `MIGRATE_TO_POSTGRESQL.bat` and follow the prompts!

