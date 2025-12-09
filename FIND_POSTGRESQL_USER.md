# 🔍 How to Find Your PostgreSQL User

## 🎯 **Quick Methods**

---

## **Method 1: Using pgAdmin (GUI)** ⭐ **Easiest**

### **Step 1: Open pgAdmin**
- Open pgAdmin application

### **Step 2: View Users**
1. Expand your PostgreSQL server (usually "PostgreSQL 15" or similar)
2. Expand **"Login/Group Roles"**
3. You'll see all users listed
4. **Default user is usually:** `postgres`

### **Step 3: Check User Details**
- Right-click on a user → **Properties**
- See username, password settings, etc.

---

## **Method 2: Using Command Line (psql)**

### **Step 1: Connect to PostgreSQL**
```cmd
psql -U postgres
```

If it asks for password, enter your PostgreSQL password.

### **Step 2: List All Users**
```sql
\du
```

This shows all users with their roles.

### **Step 3: Or Use SQL Query**
```sql
SELECT usename FROM pg_user;
```

### **Step 4: Exit**
```sql
\q
```

---

## **Method 3: Check Current User**

### **In psql:**
```sql
SELECT current_user;
```

Or:
```sql
SELECT user;
```

---

## **Method 4: Using Python (Quick Check)**

I'll create a script to check your PostgreSQL users.

---

## 📋 **Common PostgreSQL Users**

### **Default Users:**
- **`postgres`** - Default superuser (most common)
- **`postgres`** - Usually the main admin user

### **If You Created Custom User:**
- Check in pgAdmin under "Login/Group Roles"
- Or use `\du` command in psql

---

## 🔑 **Find Your Password**

### **If You Forgot Password:**
1. **pgAdmin:** Right-click user → Properties → see if password is set
2. **Reset password:**
   ```sql
   ALTER USER postgres WITH PASSWORD 'new_password';
   ```

---

## ✅ **Quick Check Script**

I'll create a Python script to check your PostgreSQL connection and users.

---

## 🎯 **Most Common Setup**

**Default PostgreSQL installation usually has:**
- **User:** `postgres`
- **Password:** The one you set during installation
- **Host:** `localhost`
- **Port:** `5432`

---

## 📝 **Test Your User**

Try connecting:
```cmd
psql -U postgres -d postgres
```

If it works, your user is `postgres`!

---

**I'll create a script to help you find your user!** 🔍

