# 📤 Push Your Code to GitHub - Step by Step

## 🎯 **SIMPLE COMMANDS**

### **STEP 1: Push Your Code**

Open PowerShell in your project folder and run:

```powershell
git push -u origin main
```

---

## 🔐 **IF YOU GET AUTHENTICATION ERROR**

You'll need a **Personal Access Token** (GitHub doesn't accept passwords anymore).

### **Get Your Token:**

1. **Go to:** https://github.com/settings/tokens
2. **Click:** "Generate new token" → "Generate new token (classic)"
3. **Name it:** `Madam DA Project`
4. **Select scope:** ✅ `repo` (Full control of private repositories)
5. **Click:** "Generate token"
6. **⚠️ COPY THE TOKEN** - You won't see it again!
7. **Save it somewhere safe!**

### **Push Again:**

```powershell
git push -u origin main
```

**When asked:**
- **Username:** `Vicihka`
- **Password:** `[paste your token here]` (NOT your GitHub password!)

---

## ✅ **AFTER FIRST PUSH**

Once you've pushed successfully, future pushes are easier:

```powershell
# Just save and push
git add .
git commit -m "Your changes"
git push
```

---

## 📋 **COMPLETE WORKFLOW**

### **Every time you make changes:**

```powershell
# 1. Save locally
git add .
git commit -m "Description of changes"

# 2. Push to GitHub
git push
```

### **Or use the script:**

1. Double-click `SAVE_WORK.bat` (saves locally)
2. Then run: `git push` (uploads to GitHub)

---

## 🎉 **YOUR CODE IS NOW ON GITHUB!**

**Repository URL:** https://github.com/Vicihka/FULL-WEB---MADAM-DA

You can:
- ✅ View your code online
- ✅ Access from anywhere
- ✅ Never lose your code
- ✅ Share with others
- ✅ Track all changes

---

## 💡 **TIPS**

- **Save token securely** - Use a password manager
- **Push regularly** - After every major change
- **Write clear commit messages** - Helps track changes
- **Never share your token** - Keep it private!

---

**Ready? Run: `git push -u origin main` 🚀**

