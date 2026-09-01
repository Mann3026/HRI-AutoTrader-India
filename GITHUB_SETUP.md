# GitHub Setup Guide - HRI AutoTrader

## Step 1: Create GitHub Account (if needed)

1. Go to https://github.com/signup
2. Enter email, create password, choose username
3. Verify email
4. Done! You now have a free GitHub account

---

## Step 2: Install Git on Your Machine

### Windows PowerShell
```powershell
winget install Git.Git -e
```

After installation, restart PowerShell or run:
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine')
```

Verify:
```powershell
git --version
```

---

## Step 3: Configure Git Locally

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Use the same email you registered on GitHub.

---

## Step 4: Create Repository on GitHub

1. Go to https://github.com/new
2. Fill in:
   - **Repository name:** `HRI-AutoTrader-India`
   - **Description:** "NSE Paper Trading Platform with Admin Panel and Portfolio Tracking"
   - **Public** (so anyone can see/test)
   - **Initialize with:** Nothing (we'll push local code)
3. Click "Create repository"
4. Copy the repository URL (you'll need it next)

---

## Step 5: Push Your Local Code to GitHub

Navigate to your project folder and run:

```powershell
cd "c:\Users\Hridansh Naik\Downloads\HRI-AutoTrader-India"

# Initialize git (if not done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: HRI AutoTrader with admin login, portfolio tracking, and signal configuration"

# Rename branch to main
git branch -M main

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/HRI-AutoTrader-India.git

# Push code to GitHub
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

---

## Step 6: Verify on GitHub

1. Go to https://github.com/YOUR_USERNAME/HRI-AutoTrader-India
2. You should see all your files there
3. Share this URL with testers!

---

## How to Keep Code Safe & Organized

### A. Make Updates Locally, Push to GitHub

After making changes locally:

```powershell
cd "c:\Users\Hridansh Naik\Downloads\HRI-AutoTrader-India"

# See what changed
git status

# Add changes
git add .

# Create a commit with a message
git commit -m "Description of what changed"

# Push to GitHub
git push
```

### B. Create Branches for Features

Keep main branch clean, create feature branches:

```powershell
# Create new branch
git checkout -b feature/database-storage

# Make changes and commit
git add .
git commit -m "Add database storage for users"

# Push branch to GitHub
git push -u origin feature/database-storage

# When done, merge back to main
git checkout main
git merge feature/database-storage
git push
```

### C. Good Commit Messages

Write clear commit messages so others understand changes:

```
❌ Bad:   "update"
✅ Good:  "Add user portfolio reporting and P&L calculations"

❌ Bad:   "fix"
✅ Good:  "Fix real-money approval gate requiring correct confirmation code"

❌ Bad:   "changes"
✅ Good:  "Implement free/paid signal provider configuration"
```

---

## GitHub Features for Your Project

### 1. Issues (Track bugs & features)
- Go to "Issues" tab
- Create issue for each feature/bug
- Assign to yourself
- Track progress
- Close when done

### 2. README Visibility
- GitHub shows README.md on repo homepage
- Already created and updated for you
- Testers see features list first thing

### 3. Releases
When ready to deploy:

```powershell
git tag -a v1.0 -m "First release: Paper trading with admin panel"
git push origin v1.0
```

Then create release on GitHub website with release notes.

### 4. Collaborators (Add team members)
- Go to Settings → Collaborators
- Add email addresses of team members
- They get access to push code

---

## Code Organization Tips

### Folder Structure (Keep It)
```
HRI-AutoTrader-India/
├── backend/
│   ├── app.py              (Main FastAPI)
│   ├── trading_engine.py   (Trade logic)
│   ├── signal_provider.py  (Signals)
│   └── requirements.txt    (Dependencies)
├── frontend/
│   ├── index.html          (Dashboard UI)
│   ├── app.js              (JavaScript)
│   └── styles.css          (Styling)
├── tests/
│   └── test_trading_engine.py  (Tests)
├── README.md               (Project info)
├── DEPLOYMENT.md           (Deploy guide)
├── DEPLOY_GUIDE.md         (Tester guide)
├── render.yaml             (Render config)
├── Procfile                (Process definition)
└── .gitignore              (What NOT to push)
```

### .gitignore (Already Created)
Git automatically ignores:
- `__pycache__/`
- `.pytest_cache/`
- `.venv/` (virtual env)
- `.env` (secrets)
- `.DS_Store` (Mac files)

**Don't commit:**
- Passwords or API keys
- Virtual environment folders
- Node modules or build files
- IDE settings (.vscode/, .idea/)

---

## Typical Workflow

### Day 1: Initial Setup
```
git init
git add .
git commit -m "Initial commit"
git push -u origin main
```

### Day 2: Add feature
```
git checkout -b feature/new-feature
# Make changes
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature
# Create Pull Request on GitHub
# Review, merge to main
git checkout main
git pull
```

### Day 3: Bug fix
```
git checkout -b bugfix/fix-issue
# Fix bug
git add .
git commit -m "Fix bug description"
git push
# Merge to main
git checkout main
git merge bugfix/fix-issue
git push
```

---

## Useful Git Commands

```powershell
# See commit history
git log

# See changes (not committed)
git diff

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Check current branch
git branch

# List all branches
git branch -a

# Clone a repo (download from GitHub)
git clone https://github.com/username/repository.git

# Pull latest changes
git pull
```

---

## Deploy from GitHub

Once code is on GitHub, you can:

1. **Deploy to Render** → GitHub integration (auto-deploys on push)
2. **Deploy to Vercel** → Frontend deployment
3. **GitHub Pages** → Host static frontend
4. **Docker** → Containerize and deploy anywhere

See DEPLOYMENT.md for details.

---

## Support & Next Steps

1. ✅ Create GitHub account
2. ✅ Install Git locally
3. ✅ Follow Step 2-5 above
4. ✅ Push code to GitHub
5. ✅ Go to DEPLOYMENT.md for Render setup
6. ✅ Share live URL with testers

Questions? Ask! 🚀
