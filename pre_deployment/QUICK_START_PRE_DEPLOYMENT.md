# ⚡ Quick Start: Pre-Deployment Testing

**TL;DR Version** - Get started quickly with the most critical steps.

---

## 🎯 5-Minute Checklist

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Tests
```bash
python manage.py test
```

### 3. Security Check
- Set `DEBUG=False` in production
- Set strong `SECRET_KEY`
- Set `ALLOWED_HOSTS`

### 4. Test Payment
- Test payment flow in test mode
- Verify order creation works

### 5. Test Admin
- Login to admin panel
- Create/edit products
- Manage orders

---

## 📚 Full Documentation

See **PRE_DEPLOYMENT_MASTER_GUIDE.md** for complete documentation.

---

## ⚠️ Critical Before Production

1. **DEBUG=False** - Must be False in production
2. **SECRET_KEY** - Must be strong random value
3. **ALLOWED_HOSTS** - Must include your domain
4. **SSL/HTTPS** - Required for production
5. **Database Backups** - Must be configured
6. **Payment Testing** - Must test in staging first

---

## 🚀 Deployment Steps

1. Complete **FINAL_GO_NOGO_CHECKLIST.md**
2. Follow **PRODUCTION_DEPLOYMENT_CHECKLIST.md**
3. Deploy and monitor

---

## 📞 Need Help?

- See **PRE_DEPLOYMENT_MASTER_GUIDE.md** for full guide
- Check individual documents for specific topics
- Review error messages in logs

---

**Good luck with your deployment! 🚀**
