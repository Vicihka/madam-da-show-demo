# How to Fix WebSocket Connection Errors

## Problem
You're seeing WebSocket connection errors because the server is running with `python manage.py runserver`, which **does NOT support WebSockets**.

## Solution

### Step 1: Stop Current Server
1. Find the terminal/command prompt where the server is running
2. Press **Ctrl+C** to stop it
3. Wait for it to fully stop

### Step 2: Start Server with WebSocket Support
**Option A: Use Batch File (Easiest)**
1. Double-click `START_SERVER_WEBSOCKET_DAPHNE.bat`
2. Wait for it to start (you'll see "Starting Daphne ASGI server...")

**Option B: Manual Command**
1. Open terminal in project folder
2. Run:
   ```bash
   venv\Scripts\activate
   daphne -b 0.0.0.0 -p 8000 project.asgi:application
   ```

### Step 3: Verify
- Check the terminal - should show "Starting Daphne ASGI server..."
- Refresh employee dashboard page
- WebSocket status should show "🟢 Connected"

## Requirements
- ✅ Redis must be running (already confirmed)
- ✅ Daphne must be installed (already confirmed)
- ✅ Server must be started with Daphne (not runserver)

## Notes
- **Normal server** (`runserver`) = No WebSocket support
- **Daphne server** = Full WebSocket support ✅

If you don't need WebSocket features, you can use `START_SERVER_NORMAL.bat` instead.

