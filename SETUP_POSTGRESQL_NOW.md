# 🚀 Quick Setup: PostgreSQL for 1000+ Customers

## ✅ **Your Credentials**
- **User:** postgres
- **Password:** root
- **Database Name:** madamda_db (will be created)

---

## 📋 **Step-by-Step Setup**

### **Step 1: Create .env File** ✅

I've created a PowerShell script for you. Run it:

```powershell
.\setup_postgresql_env.ps1
```

This will create a `.env` file with your database credentials.

**OR** manually create `.env` file with:
```env
DB_NAME=madamda_db
DB_USER=postgres
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=5432
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,*
REDIS_URL=redis://127.0.0.1:6379/1
```

---

### **Step 2: Create Database** 🔴 **REQUIRED**

Open PowerShell and run:

```powershell
# Connect to PostgreSQL
psql -U postgres

# Then run this SQL command:
CREATE DATABASE madamda_db;

# Exit psql
\q
```

**OR** use the SQL file:
```powershell
psql -U postgres -f create_database.sql
```

**OR** one-liner:
```powershell
psql -U postgres -c "CREATE DATABASE madamda_db;"
```

---

### **Step 3: Install python-dotenv** (if not installed)

```bash
pip install python-dotenv
```

---

### **Step 4: Test Database Connection** ✅

```bash
python test_db_connection.py
```

You should see:
- ✅ Database Connection: SUCCESS
- ✅ Using PostgreSQL - Ready for 1000+ customers!

---

### **Step 5: Run Migrations** 🔴 **REQUIRED**

```bash
python manage.py migrate
```

This will create all the tables in PostgreSQL.

---

### **Step 6: (Optional) Migrate Data from SQLite**

If you have existing data in SQLite:

```bash
# Export from SQLite
python manage.py dumpdata app > sqlite_data.json

# Import to PostgreSQL (after migrations)
python manage.py loaddata sqlite_data.json
```

---

## 🧪 **Verify Everything Works**

1. **Test connection:**
   ```bash
   python test_db_connection.py
   ```

2. **Start server:**
   ```bash
   python manage.py runserver
   ```

3. **Check admin panel:**
   - Go to: http://127.0.0.1:8000/admin/
   - Login and verify you can see your data

---

## ⚠️ **Troubleshooting**

### **Error: "database does not exist"**
- Run Step 2 to create the database

### **Error: "password authentication failed"**
- Verify password is "root" (as you provided)
- Check PostgreSQL is running

### **Error: "could not connect to server"**
- Check PostgreSQL is running:
  ```powershell
  # Windows: Check Services
  Get-Service postgresql*
  ```
- Or start PostgreSQL service

### **Still using SQLite?**
- Check `.env` file exists and has correct values
- Restart your server after creating `.env`
- Verify with: `python test_db_connection.py`

---

## ✅ **Success Checklist**

- [ ] `.env` file created with database credentials
- [ ] Database `madamda_db` created in PostgreSQL
- [ ] `python test_db_connection.py` shows SUCCESS
- [ ] `python manage.py migrate` completed without errors
- [ ] Server starts and connects to PostgreSQL
- [ ] Admin panel shows data (if migrated)

---

## 🎉 **After Setup**

Your website is now ready to handle **1000+ concurrent customers**!

**Performance improvements:**
- ✅ PostgreSQL (instead of SQLite)
- ✅ Connection pooling enabled
- ✅ Query optimization
- ✅ Pagination
- ✅ Caching
- ✅ WebSocket limits

---

## 📞 **Need Help?**

If you encounter any issues:

1. **Check PostgreSQL is running:**
   ```powershell
   Get-Service postgresql*
   ```

2. **Test connection manually:**
   ```powershell
   psql -U postgres -d madamda_db
   ```

3. **Check .env file:**
   ```powershell
   Get-Content .env
   ```

4. **Run test script:**
   ```bash
   python test_db_connection.py
   ```

---

**🎯 You're almost there! Just create the database and run migrations!**





