# 📱 How to Test COD Confirmation Page on Mobile

## ✅ Quick Steps

### Step 1: Find Your Computer's IP Address

Your computer's IP address is: **192.168.8.173**

(If this changes, run: `ipconfig | findstr /i "IPv4"`)

---

### Step 2: Make Sure Server is Running

1. **Start the server** using one of these:
   - `START_SERVER.bat` (for basic testing)
   - `START_SERVER_WEBSOCKET_DAPHNE.bat` (for full features)

2. **Check the server is running:**
   - You should see: `Starting server on http://0.0.0.0:8000`
   - Server must be running on `0.0.0.0` (not `127.0.0.1`)

---

### Step 3: Connect Mobile to Same Wi-Fi Network

**Important:** Your phone and computer must be on the **same Wi-Fi network**

1. Check your phone's Wi-Fi settings
2. Make sure it's connected to the same network as your computer

---

### Step 4: Access from Mobile Browser

Open your mobile browser and go to:

```
http://192.168.8.173:8000/cod/confirm/
```

**Or for a specific order:**
```
http://192.168.8.173:8000/cod/confirm/MD00001/
```

---

## 🔧 Troubleshooting

### Problem: "Can't connect" or "Page not found"

**Solution 1: Check Windows Firewall**
1. Open Windows Defender Firewall
2. Click "Allow an app or feature"
3. Make sure Python is allowed
4. Or temporarily disable firewall for testing

**Solution 2: Check Server is Running**
- Look at the server window
- Should show: `Starting server on http://0.0.0.0:8000`
- If it shows `127.0.0.1`, stop and restart with `0.0.0.0`

**Solution 3: Check IP Address**
- Your current IP: **192.168.8.173**
- If it changed, find new IP:
  ```cmd
  ipconfig | findstr /i "IPv4"
  ```

**Solution 4: Check Network**
- Make sure phone and computer are on same Wi-Fi
- Try pinging from phone (if possible)

---

### Problem: "Connection refused"

**Solution:**
1. Make sure server is running
2. Check if port 8000 is open
3. Try restarting the server

---

### Problem: Page loads but looks broken

**Solution:**
1. Clear mobile browser cache
2. Try a different browser
3. Check if CSS/JS files are loading

---

## 📋 Quick Test Checklist

- [ ] Server is running on `0.0.0.0:8000`
- [ ] Phone and computer on same Wi-Fi
- [ ] Using correct IP: `192.168.8.173`
- [ ] Windows Firewall allows Python
- [ ] URL is correct: `http://192.168.8.173:8000/cod/confirm/`

---

## 🎯 Test URLs

### COD Confirmation Page:
```
http://192.168.8.173:8000/cod/confirm/
```

### With Order Number:
```
http://192.168.8.173:8000/cod/confirm/MD00001/
```

### Employee Dashboard:
```
http://192.168.8.173:8000/employee/
```

### Main Shop:
```
http://192.168.8.173:8000/
```

---

## 💡 Tips

1. **Bookmark the URL** on your phone for easy access
2. **Use Chrome or Safari** for best compatibility
3. **Check server logs** if something doesn't work
4. **IP may change** - if it stops working, check IP again

---

## 🔍 Verify Server is Accessible

### From Computer:
```cmd
curl http://192.168.8.173:8000/cod/confirm/
```

### From Mobile:
- Open browser
- Go to: `http://192.168.8.173:8000/cod/confirm/`
- Should see the COD confirmation page

---

## ✅ Success!

If you can see the page on mobile, you're all set! 🎉

Try:
1. Enter an order number
2. Scan QR code (if available)
3. Confirm payment
4. Test all features

