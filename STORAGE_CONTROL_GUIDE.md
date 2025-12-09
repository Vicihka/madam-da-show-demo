# 🗂️ Storage Control & Management Guide

**Date:** December 7, 2025  
**Project:** MADAM DA E-Commerce Platform

---

## 📋 **QUICK REFERENCE**

### **Management Commands:**
```bash
# Check storage usage
python manage.py storage_info

# Cleanup expired QR codes
python manage.py cleanup_expired_qr_codes --days=7

# Backup database
python manage.py backup_database --compress
```

### **Windows Scripts:**
- `check_storage.bat` - Check storage information
- `cleanup_expired_qr_codes.bat` - Cleanup expired QR codes
- `backup_database.bat` - Backup database

---

## 🎯 **STORAGE CONTROL TASKS**

### **1. Daily Tasks**

#### **Check Storage Usage**
```bash
python manage.py storage_info
```
**Or use:** `check_storage.bat`

**What it shows:**
- Database size and record counts
- Media files size and count
- Static files size
- Log files size
- Total storage usage

---

### **2. Weekly Tasks**

#### **Cleanup Expired QR Codes**
```bash
python manage.py cleanup_expired_qr_codes --days=7
```
**Or use:** `cleanup_expired_qr_codes.bat`

**What it does:**
- Removes expired QR code images (older than 7 days)
- Deletes orphaned QR code files
- Frees up disk space

**Options:**
- `--days=7` - Delete QR codes older than 7 days (default)
- `--dry-run` - Preview what would be deleted
- `--force` - Force cleanup even if not expired

**Example:**
```bash
# Preview cleanup (safe)
python manage.py cleanup_expired_qr_codes --days=7 --dry-run

# Actually cleanup
python manage.py cleanup_expired_qr_codes --days=7
```

---

### **3. Weekly/Monthly Tasks**

#### **Backup Database**
```bash
python manage.py backup_database --compress
```
**Or use:** `backup_database.bat`

**What it does:**
- Creates JSON backup of all database data
- Compresses backup to save space
- Saves to `backups/` directory

**Options:**
- `--output=backups/` - Custom output directory
- `--compress` - Compress backup (recommended)

**Restore Backup:**
```bash
python manage.py loaddata backups/db_backup_20251207_120000.json
```

---

## 📊 **STORAGE MONITORING**

### **Storage Breakdown:**

#### **Database:**
- **Location:** `db.sqlite3` (dev) or PostgreSQL (prod)
- **Size:** ~2-6 MB (grows with orders)
- **Growth:** ~200-500 KB per 100 orders

#### **Media Files:**
- **Location:** `media/`
- **Size:** ~50-100 MB (depends on products)
- **Growth:** ~5-10 MB per 100 orders (QR codes)

#### **Static Files:**
- **Location:** `staticfiles/`
- **Size:** ~5-10 MB (fixed)
- **Growth:** Minimal (only when adding new static files)

#### **Log Files:**
- **Location:** `logs/`
- **Size:** ~1-5 MB (depends on activity)
- **Growth:** ~100-500 KB per month

---

## 🧹 **CLEANUP STRATEGIES**

### **1. QR Code Cleanup**

**When to run:** Weekly

**Command:**
```bash
python manage.py cleanup_expired_qr_codes --days=7
```

**What gets deleted:**
- Expired payment QR codes (older than 7 days)
- Expired tracking QR codes (older than 7 days)
- Orphaned QR code files (files without database records)

**Space saved:** ~5-10 MB per 100 orders

---

### **2. Log Rotation**

**When to run:** Monthly

**Manual Process:**
1. Archive old logs
2. Clear or truncate log files
3. Keep last 3 months of logs

**Example:**
```bash
# Archive old logs
move logs\django.log logs\django_2025_11.log
move logs\security.log logs\security_2025_11.log

# Create new log files (Django will create automatically)
```

---

### **3. Database Optimization**

**When to run:** Quarterly or when database > 100 MB

**Process:**
1. Backup database first
2. Run database optimization (VACUUM for SQLite, REINDEX for PostgreSQL)
3. Check for unused data

**SQLite:**
```bash
python manage.py dbshell
VACUUM;
```

**PostgreSQL:**
```sql
VACUUM ANALYZE;
REINDEX DATABASE madamda_db;
```

---

## 💾 **BACKUP STRATEGY**

### **1. Database Backups**

**Frequency:** Daily or Weekly

**Command:**
```bash
python manage.py backup_database --compress
```

**Storage:**
- Keep last 7 daily backups
- Keep last 4 weekly backups
- Keep last 12 monthly backups

**Location:** `backups/` directory

---

### **2. Media File Backups**

**Frequency:** Weekly

**Process:**
1. Copy `media/` directory to backup location
2. Compress if needed
3. Store off-server if possible

**Example:**
```bash
# Windows
xcopy media\*.* backups\media_backup_20251207\ /E /I

# Linux/Mac
tar -czf backups/media_backup_20251207.tar.gz media/
```

---

## 📈 **STORAGE GROWTH MONITORING**

### **Monthly Check:**

1. **Run storage info:**
   ```bash
   python manage.py storage_info
   ```

2. **Compare with previous month:**
   - Database growth
   - Media files growth
   - Log files growth

3. **Take action if needed:**
   - Cleanup if storage > 80% full
   - Optimize if growth is unexpected
   - Upgrade storage if needed

---

## ⚠️ **STORAGE WARNINGS**

### **When Storage is High:**

1. **Run cleanup immediately:**
   ```bash
   python manage.py cleanup_expired_qr_codes --days=7
   ```

2. **Check for large files:**
   ```bash
   # Windows
   dir /s /-c media\ | find "MB"
   
   # Linux/Mac
   find media/ -type f -size +10M
   ```

3. **Archive old logs:**
   - Move old logs to archive
   - Keep only recent logs

4. **Optimize images:**
   - Convert large images to WebP
   - Compress product images

---

## 🔧 **AUTOMATION**

### **Windows Task Scheduler:**

1. **Weekly QR Code Cleanup:**
   - Task: Run `cleanup_expired_qr_codes.bat`
   - Schedule: Every Sunday at 2 AM

2. **Daily Database Backup:**
   - Task: Run `backup_database.bat`
   - Schedule: Every day at 3 AM

3. **Monthly Storage Check:**
   - Task: Run `check_storage.bat`
   - Schedule: First day of month at 9 AM

---

### **Linux Cron Jobs:**

```bash
# Edit crontab
crontab -e

# Add these lines:

# Weekly QR code cleanup (Sunday 2 AM)
0 2 * * 0 cd /path/to/project && python manage.py cleanup_expired_qr_codes --days=7

# Daily database backup (3 AM)
0 3 * * * cd /path/to/project && python manage.py backup_database --compress

# Monthly storage check (1st of month, 9 AM)
0 9 1 * * cd /path/to/project && python manage.py storage_info >> logs/storage_check.log
```

---

## ✅ **STORAGE HEALTH CHECKLIST**

### **Daily:**
- [ ] Check for errors in logs
- [ ] Monitor disk space (if < 20% free, take action)

### **Weekly:**
- [ ] Run QR code cleanup
- [ ] Check storage usage
- [ ] Review log file sizes

### **Monthly:**
- [ ] Run full storage info report
- [ ] Archive old logs
- [ ] Review backup strategy
- [ ] Check for orphaned files

### **Quarterly:**
- [ ] Optimize database
- [ ] Review storage growth trends
- [ ] Update backup strategy if needed
- [ ] Clean up old backups

---

## 📊 **STORAGE TARGETS**

### **Recommended Limits:**

- **Database:** < 100 MB (before optimization)
- **Media Files:** < 500 MB (before cleanup)
- **Log Files:** < 50 MB (before rotation)
- **Total Storage:** < 1 GB (before review)

### **Action Thresholds:**

- **Warning:** Storage > 80% full
- **Critical:** Storage > 90% full
- **Emergency:** Storage > 95% full

---

## 🚨 **EMERGENCY CLEANUP**

### **If Storage is Critical (> 95% full):**

1. **Immediate Actions:**
   ```bash
   # Cleanup all QR codes older than 1 day
   python manage.py cleanup_expired_qr_codes --days=1
   
   # Archive and clear logs
   # (manual process)
   
   # Check for large files
   python manage.py storage_info
   ```

2. **Review Large Files:**
   - Check product images (optimize if needed)
   - Check hero slide videos (compress if needed)
   - Check log files (archive old logs)

3. **Database Optimization:**
   ```bash
   # Backup first!
   python manage.py backup_database --compress
   
   # Then optimize
   python manage.py dbshell
   # Run VACUUM or REINDEX
   ```

---

## 📝 **NOTES**

- **QR codes** expire after 5 minutes but files are kept for 7 days (for debugging)
- **Log files** should be rotated monthly to prevent disk space issues
- **Backups** should be stored off-server for safety
- **Media files** are user-uploaded and should be backed up regularly
- **Static files** can be regenerated and don't need backup

---

**Last Updated:** December 7, 2025  
**Next Review:** Monthly or when storage exceeds 1GB

