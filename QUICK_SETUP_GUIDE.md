# 🚀 Quick Setup Guide - PostgreSQL Configuration

## ✅ **What I've Done For You**

1. ✅ Created `.env` file with your credentials:
   - User: `postgres`
   - Password: `root`
   - Database: `madamda_db` (will be created)

2. ✅ Created helper scripts:
   - `setup_postgresql_env.ps1` - PowerShell setup script
   - `test_db_connection.py` - Test database connection
   - `create_database.sql` - SQL script to create database
   - `SETUP_DATABASE.bat` - Windows batch file for quick setup

---

## 📋 **Quick Setup (Choose One Method)**

### **Method 1: Use Batch File (Easiest)** ⭐

Just double-click:
```
SETUP_DATABASE.bat
```

This will:
1. Create the database
2. Install python-dotenv
3. Test the connection
4. Run migrations

---

### **Method 2: Manual Setup**

#### **Step 1: Create Database**

Open PowerShell and run:
```powershell
psql -U postgres -c "CREATE DATABASE madamda_db;"
```

**OR** use the SQL file:
```powershell
psql -U postgres -f create_database.sql
```

**OR** connect to psql:
```powershell
psql -U postgres
```
Then run:
```sql
CREATE DATABASE madamda_db;
\q
```

---

#### **Step 2: Install python-dotenv** (if not installed)

```bash
pip install python-dotenv
```

---

#### **Step 3: Test Connection**

```bash
python test_db_connection.py
```

You should see:
```
✅ Database Connection: SUCCESS
✅ Using PostgreSQL - Ready for 1000+ customers!
```

---

#### **Step 4: Run Migrations**

```bash
python manage.py migrate
```

This creates all tables in PostgreSQL.

---

#### **Step 5: (Optional) Migrate Data from SQLite**

If you have existing data:

```bash
# Export from SQLite
python manage.py dumpdata app > sqlite_data.json

# Import to PostgreSQL
python manage.py loaddata sqlite_data.json
```

---

## ✅ **Verify Everything Works**

1. **Test connection:**
   ```bash
   python test_db_connection.py
   ```

2. **Start server:**
   ```bash
   python manage.py runserver
   ```

3. **Check admin:**
   - Go to: http://127.0.0.1:8000/admin/
   - Login and verify data

---

## ⚠️ **Troubleshooting**

### **"database does not exist"**
- Run Step 1 to create the database

### **"password authentication failed"**
- Verify password is "root"
- Check PostgreSQL is running

### **"could not connect to server"**
- Check PostgreSQL service is running:
  ```powershell
  Get-Service postgresql*
  ```
- Start it if needed

### **Still using SQLite?**
- Restart your server after creating `.env`
- Verify with: `python test_db_connection.py`
- Check `.env` file exists and has correct values

---

## 🎉 **After Setup**

Your website is now ready for **1000+ customers**!

**What's configured:**
- ✅ PostgreSQL database
- ✅ Connection pooling
- ✅ Query optimization
- ✅ Pagination
- ✅ Caching
- ✅ WebSocket limits

---

## 📞 **Need Help?**

Run the test script:
```bash
python test_db_connection.py
```

It will show you exactly what's wrong if there's an issue.

---

**🎯 Ready to go! Just run `SETUP_DATABASE.bat` or follow the manual steps above!**

