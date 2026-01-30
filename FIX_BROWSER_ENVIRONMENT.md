# How to Fix Browser Testing Tool - Set HOME Environment Variable

## Problem
The browser automation tool (Playwright) requires the `$HOME` environment variable, which is not set by default on Windows.

**Error:** `failed to create browser context: failed to install playwright: $HOME environment variable is not set`

---

## Solution: Set HOME Environment Variable Permanently

### Step 1: Open System Properties

**Method 1 - Using Run Dialog (Fastest):**
1. Press `Win + R` on your keyboard
2. A small "Run" dialog box will appear
3. Type exactly: `sysdm.cpl`
4. Press `Enter`

**Method 2 - Using Search:**
1. Click Windows Start button
2. Type: "environment variables"
3. Click "Edit the system environment variables"

### Step 2: Access Environment Variables

1. The "System Properties" window will open
2. Make sure you're on the "**Advanced**" tab (should be by default)
3. At the bottom of the window, click the "**Environment Variables...**" button

### Step 3: Add the HOME Variable

1. You'll see two sections:
   - **Top**: "User variables for hp" 
   - **Bottom**: "System variables"

2. In the **TOP section** ("User variables for hp"), click "**New...**" button

3. A small "New User Variable" dialog will appear:
   - **Variable name:** Type exactly: `HOME`
   - **Variable value:** Type exactly: `C:\Users\hp`
   
4. Click "**OK**"

### Step 4: Verify and Save

1. You should now see `HOME` in your list of User variables
2. The value should show: `C:\Users\hp`
3. Click "**OK**" on the Environment Variables window
4. Click "**OK**" on the System Properties window

### Step 5: Restart Everything

**CRITICAL:** The environment variable won't take effect until you restart!

**Option A - Quick Restart (Recommended):**
1. Close ALL terminal windows (Git Bash, PowerShell, CMD, etc.)
2. Close this AI assistant window/application
3. **Log out of Windows** and **log back in**
4. Reopen everything

**Option B - Full Restart:**
1. Save all your work
2. **Restart your computer**
3. After restart, everything will work

### Step 6: Verify It Worked

After restarting, open a new Git Bash terminal and run:

```bash
echo $HOME
```

**Expected output:** `/c/Users/hp` or `C:\Users\hp`

If you see this, it worked! ✅

---

## Testing the Browser Tool After Fix

Once you've completed the steps above and restarted:

1. Start your Flask app again:
   ```bash
   cd "d:/AWS project"
   python app.py
   ```

2. Open a new conversation with the AI assistant

3. Ask it to test the application in browser - the browser tool should now work!

---

## Quick Visual Reference

**Windows Environment Variables Window Structure:**
```
┌─────────────────────────────────────────────┐
│         System Properties                   │
├─────────────────────────────────────────────┤
│  [Advanced] Tab                             │
│                                             │
│  Performance: [ Visual effects, ... ]       │
│                                             │
│  User Profiles: [ Settings ]                │
│                                             │
│  Startup and Recovery: [ Settings ]         │
│                                             │
│  [ Environment Variables... ] ← CLICK HERE  │
└─────────────────────────────────────────────┘

Then:

┌─────────────────────────────────────────────┐
│       Environment Variables                 │
├─────────────────────────────────────────────┤
│  User variables for hp                      │
│  ┌───────────────────────────────────────┐  │
│  │ Variable        │ Value               │  │
│  │ HOME            │ C:\Users\hp         │  │← This will appear after you add it
│  │ PATH            │ C:\...              │  │
│  │ TEMP            │ C:\...              │  │
│  └───────────────────────────────────────┘  │
│  [ New... ]  [ Edit... ]  [ Delete ]        │← Click "New..." to add HOME
│                                             │
│  System variables                           │
│  ┌───────────────────────────────────────┐  │
│  │ ...                                   │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

---

## Alternative: One-Time Terminal Fix (Temporary)

If you just want to test once without permanent changes, run this in Git Bash:

```bash
export HOME=/c/Users/hp
```

**Note:** This only works for the current terminal session. Close the terminal and it's gone.

---

## Troubleshooting

### Issue: Can't find "sysdm.cpl"
- Make sure you typed it exactly: `sysdm.cpl` (no spaces)
- Try the search method instead: Search for "environment variables"

### Issue: HOME variable doesn't show after restart
- Make sure you added it to **User variables** (top section), not System variables
- Make sure you saved by clicking OK on all windows
- Try logging out and back in, or full restart

### Issue: Browser tool still doesn't work
- Verify `echo $HOME` shows the correct path
- Make sure you closed ALL terminal windows before reopening
- Try a full computer restart instead of just logout

### Issue: Don't have admin rights
- You should be able to add User variables without admin rights
- If blocked, ask your system administrator for help
- Or just test the application in your regular browser - it works fine!

---

## Why This Is Needed

**Technical Details:**
- Playwright (browser automation library) is designed for Linux/Mac by default
- On those systems, `$HOME` is always set (points to user's home directory)
- Windows uses `%USERPROFILE%` instead
- Playwright doesn't check for `%USERPROFILE%`, only `$HOME`
- Setting `HOME` to match your user folder solves the compatibility issue

---

## Summary

1. ✅ Press `Win + R`, type `sysdm.cpl`, press Enter
2. ✅ Click "Environment Variables..." button
3. ✅ Click "New..." in User variables section
4. ✅ Name: `HOME`, Value: `C:\Users\hp`
5. ✅ Click OK on all windows
6. ✅ **Restart** (logout/login or full restart)
7. ✅ Verify with `echo $HOME`

**That's it!** After restart, the browser testing tool will work.

---

**Estimated Time:** 2-3 minutes + restart time

**Current application status:** Your Flask app is fully functional and can be tested in a regular browser at http://localhost:5000 right now, without waiting for this fix!
