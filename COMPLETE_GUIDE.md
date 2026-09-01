# HRI AutoTrader - Complete User Guide

## Table of Contents
1. [How to Deploy](#deployment)
2. [How to Use Code from GitHub](#github-usage)
3. [How Upgrades Work (Pull/Push)](#upgrades)
4. [How Outsiders Can Access](#sharing)
5. [Desktop App Installation](#desktop)

---

## 1. How to Deploy {#deployment}

### Option A: Deploy on Render (Easiest - Free)

**What is Render?**
- Free cloud hosting service
- Your app runs on their servers 24/7
- Anyone can access via URL

**Steps:**

1. **Create Render Account**
   - Go to https://render.com/signup
   - Click "Continue with GitHub"
   - Authorize with your GitHub account

2. **Deploy Your Project**
   - Click "New +" → "Web Service"
   - Select your GitHub repository: `HRI-AutoTrader-India`
   - Fill in:
     - Name: `hri-autotrader`
     - Region: `oregon` (or near you)
     - Build Command: `pip install -r backend/requirements.txt`
     - Start Command: `python -m uvicorn backend.app:app --host 0.0.0.0 --port $PORT`
   - Click "Create Web Service"
   - Wait 2-3 minutes

3. **Get Your Live URL**
   - After deployment, you get URL like: `https://hri-autotrader-xxxxx.onrender.com`
   - This is your live app URL!

4. **Access the App**
   - Backend API: `https://hri-autotrader-xxxxx.onrender.com/`
   - Frontend: Download `frontend/index.html` from GitHub and open locally (auto-connects to live backend)

---

### Option B: Deploy on Your Own Server

**Requirements:**
- Server with Linux/Windows
- Python 3.11+ installed
- Domain name (optional)

**Steps:**

1. **Clone GitHub Repository**
   ```bash
   git clone https://github.com/Mann3026/HRI-AutoTrader-India.git
   cd HRI-AutoTrader-India
   ```

2. **Install Dependencies**
   ```bash
   python -m pip install -r backend/requirements.txt
   ```

3. **Start Backend**
   ```bash
   python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000
   ```

4. **Access Frontend**
   - Open `frontend/index.html` in browser
   - Or deploy frontend to Vercel/Netlify

---

## 2. How to Use Code from GitHub {#github-usage}

### What is GitHub?
- Cloud storage for code
- Everyone can see your code
- Easy to share and collaborate
- Backup of your project

### How Your Code is Stored

Your project location:
```
GitHub: https://github.com/Mann3026/HRI-AutoTrader-India
Your Computer: c:\Users\Hridansh Naik\Downloads\HRI-AutoTrader-India
```

### How to Get Code from GitHub

**Method 1: Download ZIP (for non-developers)**

1. Go to https://github.com/Mann3026/HRI-AutoTrader-India
2. Click green button "Code"
3. Click "Download ZIP"
4. Extract to your computer
5. You now have all the code!

**Method 2: Clone with Git (recommended)**

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User')

git clone https://github.com/Mann3026/HRI-AutoTrader-India.git

cd HRI-AutoTrader-India
```

This creates a folder with all code + Git history.

---

## 3. How Upgrades Work (Pull/Push) {#upgrades}

### Understanding Git Workflow

```
Your Computer          →        GitHub          →      Render Server
(Local Code)         (Remote Storage)         (Live App)
```

### Scenario 1: You Make Changes Locally

**Situation:** You fix a bug or add a feature on your computer

**Steps:**

1. **Make Changes**
   - Edit files in your project folder
   - Save changes

2. **Check Status**
   ```powershell
   cd "c:\Users\Hridansh Naik\Downloads\HRI-AutoTrader-India"
   git status
   ```
   Shows which files changed

3. **Add Changes to Git**
   ```powershell
   git add .
   ```

4. **Commit Changes (Save Snapshot)**
   ```powershell
   git commit -m "Fixed bug: Real-money trading approval gate"
   ```

5. **Push to GitHub**
   ```powershell
   git push
   ```

6. **Render Auto-Deploys**
   - Render watches your GitHub repo
   - When you push, Render automatically rebuilds
   - New version goes live in 2-3 minutes

**Timeline:**
```
You commit → Push to GitHub → Render sees update → App redeployed → Live!
   (5s)        (5s)              (10s)               (2 min)
```

---

### Scenario 2: Someone Else Makes Changes

**Situation:** A team member updates code on GitHub

**Steps to Get Their Changes:**

1. **Pull Latest Code**
   ```powershell
   cd "c:\Users\Hridansh Naik\Downloads\HRI-AutoTrader-India"
   git pull
   ```
   Downloads latest code from GitHub

2. **You Now Have Their Changes**
   - All files updated
   - Ready to use

---

### Scenario 3: Multiple People Working (Collaboration)

**Day 1: You Work**
```
git add .
git commit -m "Add portfolio reporting"
git push
```

**Day 2: Colleague Works**
```
git pull              ← Gets your changes
# Makes their changes
git add .
git commit -m "Add signal configuration"
git push
```

**Day 3: You Continue**
```
git pull              ← Gets colleague's changes
# Now you have both changes
# Make more changes
git add .
git commit -m "Fix P&L calculations"
git push
```

---

### Important Git Commands

| Command | What It Does |
|---------|-------------|
| `git status` | Shows what changed |
| `git add .` | Prepare changes to save |
| `git commit -m "message"` | Save snapshot with message |
| `git push` | Send to GitHub |
| `git pull` | Get latest from GitHub |
| `git log` | See commit history |
| `git branch -a` | See all branches |

---

## 4. How Outsiders Can Access {#sharing}

### What Can Testers Do?

Outsiders can:
- ✅ View code on GitHub
- ✅ Test the live app
- ✅ Report bugs
- ✅ Make suggestions
- ✅ Clone code for their own use

Outsiders CANNOT:
- ❌ Push code (without permission)
- ❌ Delete your repo
- ❌ See your server password

---

### How to Share with Testers

**Option 1: Share Live URL Only**

```
Share this link:
https://hri-autotrader-xxxxx.onrender.com

They can:
- Test the app
- Create users
- Log trades
- View reports
- Try real-money approval gate
```

**Option 2: Share GitHub Repository**

```
Share this link:
https://github.com/Mann3026/HRI-AutoTrader-India

They can:
- See all code
- Run locally on their computer
- Suggest improvements
- Report bugs in "Issues" tab
```

**Option 3: Share Both**

```
For Testing:
Live App: https://hri-autotrader-xxxxx.onrender.com

For Developers:
GitHub: https://github.com/Mann3026/HRI-AutoTrader-India
```

---

### How Testers Report Issues

1. **They Find a Bug**
   - Example: "Profit calculation is wrong"

2. **They Go to GitHub Issues**
   - https://github.com/Mann3026/HRI-AutoTrader-India/issues
   - Click "New Issue"
   - Describe the bug
   - Click "Submit Issue"

3. **You Get Notification**
   - GitHub emails you about the issue
   - You can fix it
   - Push fix to GitHub
   - Render auto-deploys
   - They see fix live within minutes

---

### How Testers Contribute Code

1. **They Fork Your Repository**
   - Creates their own copy
   - They can modify without affecting yours

2. **They Make Changes**
   - Fix a bug or add feature
   - Commit and push to their fork

3. **They Create Pull Request**
   - Shows you the changes
   - You can review and approve
   - If good, merge to your main code

4. **You Merge**
   - Their code now part of your project
   - Push to GitHub
   - Render deploys new version

---

## 5. Desktop App Installation {#desktop}

### Can This Be Installed as Desktop App?

**SHORT ANSWER:** Yes, but with requirements

### Option 1: Run Locally (Simplest)

**What Happens:**
- App runs on your computer
- Only you can access it
- Frontend opens in browser
- Backend runs in PowerShell

**How:**

1. **Install Requirements**
   ```powershell
   python -m pip install -r backend/requirements.txt
   ```

2. **Start Backend**
   ```powershell
   python -m uvicorn backend.app:app --reload
   ```

3. **Open Frontend**
   - Double-click `frontend/index.html`
   - Browser opens automatically

**That's it!** ✅

---

### Option 2: Convert to Executable (.EXE)

**What Happens:**
- Create `.exe` file
- Others can run without Python installed
- Feels like real desktop app

**Requirements:**
- Python developer knowledge
- Tools: PyInstaller or cx_Freeze

**Steps (Advanced):**

1. **Install PyInstaller**
   ```powershell
   python -m pip install pyinstaller
   ```

2. **Create Executable**
   ```powershell
   pyinstaller --onefile backend/app.py
   ```

3. **Share .exe**
   - File size: ~50MB
   - Others can run directly
   - No Python needed

**Problem:** Backend still needs API connection, so just `.exe` is incomplete.

---

### Option 3: Electron App (Full Desktop App)

**What Happens:**
- Looks like native desktop app
- Install like any Windows program
- Everything bundled together

**Requirements:**
- Node.js & Electron knowledge
- More complex setup

**Not recommended for now** - too complex.

---

### Option 4: Recommended - Hybrid Approach

**Best for Non-Technical Users:**

1. **Backend:** Keep on Render (cloud)
   - Always running
   - Everyone can access
   - No setup needed

2. **Frontend:** Install via NSIS Installer
   - Creates Windows installer (.exe)
   - One-click install
   - Opens browser to your app
   - Very simple

**How to Create NSIS Installer:**

```
This is complex - would need separate guide
But results in: "HRI-AutoTrader-Setup.exe"
```

---

## Summary: What Works Now

| Feature | Status | Details |
|---------|--------|---------|
| Web App (Cloud) | ✅ Ready | Access anywhere via URL |
| Code on GitHub | ✅ Ready | Public, shareable |
| Pull/Push Updates | ✅ Ready | Auto-deploys to Render |
| Sharing with Testers | ✅ Ready | Just share URL |
| Desktop App (.exe) | ⚠️ Advanced | Need PyInstaller setup |
| Electron App | ❌ No | Too complex for now |
| Local Running | ✅ Ready | Python + run locally |

---

## Quick Start for Others

### If They Want to TEST
```
1. Go to: https://hri-autotrader-xxxxx.onrender.com
2. Login: admin / admin123
3. Create user account
4. Start testing!
```

### If They Want to RUN LOCALLY
```
1. Clone: git clone https://github.com/Mann3026/HRI-AutoTrader-India.git
2. Install: python -m pip install -r backend/requirements.txt
3. Run: python -m uvicorn backend.app:app --reload
4. Open: frontend/index.html
```

### If They Want to MODIFY CODE
```
1. Fork on GitHub
2. Clone their fork
3. Make changes
4. Create Pull Request
5. You review and merge
```

---

## Common Questions

### Q: Can Testers See My Code?
**A:** Only if you make repo PUBLIC (it is public). They see backend code but can't access your server.

### Q: Does Code Auto-Update on Their Computer?
**A:** No. They must run `git pull` to get latest code.

### Q: What if Two People Push at Same Time?
**A:** Git handles it. You might get "conflict" - easily resolved.

### Q: Can Outsiders Delete My Repository?
**A:** No. You're the owner. They can only view/fork.

### Q: How Much Does Render Cost?
**A:** Free tier is unlimited for hobby projects. Paid tier is $7/month if needed.

### Q: Can Offline Users Access the App?
**A:** No. They need internet. (Unless they run locally on their computer)

### Q: How Often Should I Push Updates?
**A:** Whenever you make improvements. Daily, weekly - your choice.

### Q: Can I Undo a Push?
**A:** Yes! `git revert` or `git reset`. (See Git guide)

---

## Next Steps

1. ✅ Push code to GitHub (DONE)
2. ✅ Deploy to Render (NEXT)
3. ✅ Share URL with testers
4. ✅ Gather feedback
5. ✅ Make improvements
6. ✅ Push updates (auto-deploys!)
7. ✅ Repeat!

---

**Need more help? Ask!** 🚀
