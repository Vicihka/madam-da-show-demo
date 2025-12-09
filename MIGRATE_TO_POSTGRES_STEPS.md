# 🚀 Step-by-Step: Switch to PostgreSQL

## 📋 **WHAT YOU NEED TO DO NOW**

### **Step 1: Set PostgreSQL Environment Variables**

Open PowerShell in your project directory and run:

```powershell
$env:DB_NAME = "madamda_db"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "your_actual_postgres_password"
$env:DB_HOST = "localhost"
$env:DB_PORT = "5432"
```

**Replace `your_actual_postgres_password` with your real PostgreSQL password!**

---

### **Step 2: Verify PostgreSQL Connection**

```powershell
python check_db.py
```

**Expected Output:**
- Engine: `django.db.backends.postgresql` ✅
- Database Name: `madamda_db` (or your database name)

**If you see SQLite, the environment variables aren't set correctly!**

---

### **Step 3: Export Data from SQLite**

Export all your current data (products, orders, customers, etc.):

```powershell
python manage.py dumpdata app --exclude auth.permission --exclude contenttypes > sqlite_backup.json
```

This creates a backup file with all your data.

---

### **Step 4: Create PostgreSQL Database (if not exists)**

Make sure your PostgreSQL database exists. Connect to PostgreSQL and run:

```sql
CREATE DATABASE madamda_db;
```

Or use pgAdmin to create it.

---

### **Step 5: Run Migrations on PostgreSQL**

Create all tables in PostgreSQL:

```powershell
python manage.py migrate
```

This will create all the tables (but they'll be empty).

---

### **Step 6: Import Your Data to PostgreSQL**

Import all your data from SQLite backup:

```powershell
python manage.py loaddata sqlite_backup.json
```

This will import:
- ✅ All products
- ✅ All orders
- ✅ All customers
- ✅ All other data

---

### **Step 7: Verify Everything Works**

```powershell
python check_db.py
```

You should see:
- ✅ Engine: PostgreSQL
- ✅ All your products listed
- ✅ Same count as before

---

### **Step 8: Test in Admin Panel**

1. Start server: `python manage.py runserver`
2. Go to admin panel
3. Check if all products are there
4. Try adding a new product
5. Verify it appears in PostgreSQL

---

## ⚠️ **IMPORTANT NOTES**

### **Environment Variables Reset**
- Environment variables reset when you close PowerShell
- **For permanent setup**, create a `.env` file:

Create `.env` file in project root:
```env
DB_NAME=madamda_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

Then install python-dotenv:
```powershell
pip install python-dotenv
```

### **Keep SQLite Backup**
- Don't delete `sqlite_backup.json` until you verify everything works
- Keep `db.sqlite3` as backup

---

## 🔍 **TROUBLESHOOTING**

### **"Connection refused" or "Cannot connect"**
- Make sure PostgreSQL is running
- Check if database exists
- Verify username/password
- Check firewall settings

### **"Database does not exist"**
- Create database first:
  ```sql
  CREATE DATABASE madamda_db;
  ```

### **"Still using SQLite"**
- Make sure you set environment variables in the SAME PowerShell session
- Restart terminal after setting variables
- Check with: `python check_db.py`

### **"Products not showing"**
- Make sure you ran `loaddata` command
- Check you're looking at the correct database
- Verify with: `python check_db.py`

---

## ✅ **QUICK CHECKLIST**

- [ ] Set PostgreSQL environment variables
- [ ] Verify connection (`python check_db.py`)
- [ ] Export SQLite data (`dumpdata`)
- [ ] Create PostgreSQL database (if needed)
- [ ] Run migrations (`migrate`)
- [ ] Import data (`loaddata`)
- [ ] Verify products (`check_db.py`)
- [ ] Test in admin panel
- [ ] Create `.env` file for permanent setup (optional)

---

## 🎯 **AFTER MIGRATION**

Once everything works:
1. ✅ Your products will be in PostgreSQL
2. ✅ New products added in admin will go to PostgreSQL
3. ✅ All data is now in PostgreSQL
4. ✅ You can delete SQLite file (optional, keep as backup)

---

**Ready? Start with Step 1!** 🚀

