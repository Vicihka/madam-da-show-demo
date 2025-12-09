# 🔧 Setup PostgreSQL Connection

## ❌ **PROBLEM IDENTIFIED**

Your Django app is currently using **SQLite** instead of **PostgreSQL** because the environment variables are not set.

**Current Status:**
- Database: SQLite (`db.sqlite3`)
- Products are saved in SQLite, not PostgreSQL
- That's why you don't see them in PostgreSQL!

---

## ✅ **SOLUTION: Set PostgreSQL Environment Variables**

### **Option 1: Quick Setup (PowerShell)**

Run this in PowerShell (replace with your actual PostgreSQL details):

```powershell
$env:DB_NAME = "madamda_db"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "your_postgres_password"
$env:DB_HOST = "localhost"
$env:DB_PORT = "5432"
```

Then verify:
```powershell
python check_db.py
```

### **Option 2: Use the Script**

Run the provided script:
```powershell
.\switch_to_postgresql.ps1
```

### **Option 3: Permanent Setup (Create .env file)**

Create a `.env` file in your project root:

```env
DB_NAME=madamda_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

Then install python-dotenv:
```bash
pip install python-dotenv
```

---

## 📋 **STEPS TO MIGRATE DATA**

Once PostgreSQL is connected:

### **Step 1: Export Data from SQLite**
```bash
python manage.py dumpdata app > sqlite_data.json
```

### **Step 2: Set PostgreSQL Environment Variables**
(Use one of the options above)

### **Step 3: Run Migrations on PostgreSQL**
```bash
python manage.py migrate
```

### **Step 4: Import Data to PostgreSQL**
```bash
python manage.py loaddata sqlite_data.json
```

### **Step 5: Verify**
```bash
python check_db.py
```

---

## 🔍 **VERIFY CONNECTION**

After setting environment variables, run:
```bash
python check_db.py
```

You should see:
- Engine: `django.db.backends.postgresql`
- Database Name: `madamda_db` (or your database name)
- Products should be visible

---

## ⚠️ **IMPORTANT NOTES**

1. **Environment variables are session-specific** - They reset when you close PowerShell
2. **For permanent setup**, use `.env` file or set in your shell profile
3. **Make sure PostgreSQL is running** before connecting
4. **Database must exist** - Create it first if it doesn't exist:
   ```sql
   CREATE DATABASE madamda_db;
   ```

---

## 🐛 **TROUBLESHOOTING**

### **Connection Error?**
- Check PostgreSQL is running: `pg_isready`
- Verify database exists
- Check username/password
- Check firewall settings

### **Still Using SQLite?**
- Make sure environment variables are set in the same PowerShell session
- Restart your terminal after setting variables
- Check with: `python check_db.py`

### **Products Not Showing?**
- Make sure you've imported data from SQLite
- Check you're looking at the correct database
- Verify table name: `app_product`

