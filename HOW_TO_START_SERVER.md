# 🚀 How to Start Your Server

## ✅ **Easiest Way: Use the Batch File**

### **Method 1: Double-Click (Easiest)** ⭐

1. **Find the file:** `START_SERVER_WEBSOCKET.bat`
2. **Double-click it**
3. **Wait for server to start**
4. **Done!** Server is running on `http://127.0.0.1:8000`

---

## 📋 **Method 2: Command Line**

### **Step 1: Open Terminal**
- Press `Win + R`
- Type `cmd` or `powershell`
- Press Enter

### **Step 2: Navigate to Project**
```cmd
cd "D:\Term3 IT STEP\PYTHON\DJANGO - MADAM DA"
```

### **Step 3: Run Batch File**
```cmd
START_SERVER_WEBSOCKET.bat
```

**OR run directly:**
```cmd
venv\Scripts\activate
python -m daphne -b 127.0.0.1 -p 8000 project.asgi:application
```

---

## 🎯 **What Happens When You Start**

1. ✅ Virtual environment activates automatically
2. ✅ Packages install/update if needed
3. ✅ Server starts on port 8000
4. ✅ WebSocket support enabled
5. ✅ Ready to use!

---

## 📱 **After Server Starts**

### **Access Your Website:**
- **Customer Site:** `http://127.0.0.1:8000/`
- **Employee Dashboard:** `http://127.0.0.1:8000/employee/`
- **Admin Panel:** `http://127.0.0.1:8000/admin/`

### **Check WebSocket:**
- Open employee dashboard
- Look at top-right corner
- Should show: **"🟢 Real-time: ON"**

---

## ⚠️ **Important Notes**

### **Before Starting Server:**
1. ✅ **Redis must be running** (it should be running automatically as Windows service)
2. ✅ **Check Redis:** `Get-Service Redis` (should show "Running")

### **If Redis is Not Running:**
```powershell
Start-Service Redis
```

---

## 🛑 **How to Stop Server**

### **In the Terminal Window:**
- Press `Ctrl + C`
- Server stops

### **Or Close the Window:**
- Close the terminal window
- Server stops

---

## 🔄 **Quick Commands**

### **Start Server:**
```cmd
START_SERVER_WEBSOCKET.bat
```

### **Check if Server is Running:**
```cmd
netstat -an | findstr 8000
```

### **Check Redis:**
```powershell
Get-Service Redis
```

---

## 📝 **Step-by-Step Guide**

### **Every Time You Want to Start:**

1. **Open Command Prompt or PowerShell**
2. **Navigate to project folder:**
   ```cmd
   cd "D:\Term3 IT STEP\PYTHON\DJANGO - MADAM DA"
   ```
3. **Run the batch file:**
   ```cmd
   START_SERVER_WEBSOCKET.bat
   ```
4. **Wait for:**
   ```
   Starting server on http://127.0.0.1:8000
   ```
5. **Open browser:**
   ```
   http://127.0.0.1:8000/employee/
   ```

---

## ✅ **Summary**

**Easiest way:**
1. Double-click `START_SERVER_WEBSOCKET.bat`
2. Wait for server to start
3. Open dashboard in browser
4. Done!

**That's it!** 🎉

