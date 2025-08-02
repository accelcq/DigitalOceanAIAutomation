# DigitalOcean AI Automation

A FastAPI application containerized with Docker.
AI Automation for source code generation to deploy on DigitalOcean Droplets/VPS-Virtual Private Server using DigitalOcean Container Registry

## Prerequisites

- Python 3.13+
- Docker
- Docker Compose (optional)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/accelcq/DigitalOceanAIAutomation.git
cd DigitalOceanAIAutomation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Local Development
```bash
uvicorn main:app --reload
```

### Docker
```bash
docker build -t digitaloceanaiautomation .
docker run -p 8000:8000 digitaloceanaiautomation
```

## API Documentation

Once the application is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Dependencies

- FastAPI 0.115.0
- Uvicorn 0.30.6

## Version Control & GitHub Deployment

### Authentication Setup
If you encounter permission issues, ensure you're authenticated with the correct GitHub account:

```bash
# Clear cached credentials
git config --global --unset credential.helper
git config --global credential.helper manager-core

# Update git config for accelcq account
git config --global user.name "AccelCQ"
git config --global user.email "accelcq-email@example.com"
```

**VS Code GitHub Authentication:**
1. Press `Ctrl+Shift+P`
2. Type "GitHub: Sign out" and execute
3. Type "GitHub: Sign in" and authenticate with AccelCQ account

### Initial Setup
```bash
# Initialize git repository
git init

# Add GitHub remote using accelcq account
git remote add origin https://github.com/accelcq/DigitalOceanAIAutomation.git

# Configure git user (if not already configured)
git config user.name "accelcq"
git config user.email "your-email@example.com"
```

### Pushing Code to GitHub
```bash
# Add all files to staging
git add .

# Commit changes
git commit -m "Initial commit: digitaloceanaiautomation project setup"

# Push to main branch
git push -u origin main
```

### Subsequent Updates
```bash
# Add changes
git add .

# Commit with descriptive message
git commit -m "Your commit message here"

# Push to GitHub
git push origin main
```

## License

This project is licensed under the MIT License.

## Development Workflow - Dev Branch Setup and Management

### **For Developers: Working with Dev Branch**

This project supports automatic deployment to both **production** and **development** environments:
- **Production (main branch)**: `http://YOUR_DROPLET_IP:80`
- **Development (dev branch)**: `http://YOUR_DROPLET_IP:8080`

### **Step 1: Switch to Dev Branch in VS Code**

#### **Option A: Using VS Code Git Integration (Recommended)**
1. **Stay in VS Code** - No need to close the editor
2. **Open Command Palette**: Press `Ctrl+Shift+P`
3. **Type**: `Git: Create Branch` (or `Git: Checkout to` if branch exists)
4. **Enter branch name**: `dev`
5. **Press Enter** - VS Code automatically switches to the `dev` branch

#### **Option B: Using Terminal in VS Code**
```bash
# Open Terminal in VS Code: Ctrl+` (backtick)

# Create and switch to dev branch (first time)
git checkout -b dev

# Or switch to existing dev branch
git checkout dev

# Verify you're on dev branch
git branch
# Should show: * dev (asterisk indicates current branch)
```

#### **Option C: Using External Terminal**
```bash
# Navigate to project directory
cd "d:\AccelCQ\project\TestProject\DigitalOceanAIAutomation"

# Create and switch to dev branch
git checkout -b dev

# Verify current branch
git branch
```

### **Step 2: Verify Branch Setup**

**In VS Code, check the bottom-left corner** - it should show `dev` instead of `main`

### **Step 3: Daily Development Workflow**

#### **Working on Features**
```bash
# Ensure you're on dev branch
git checkout dev

# Pull latest changes
git pull origin dev

# Make your changes
# ... edit files in VS Code ...

# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: Add new feature description"

# Push to dev branch (triggers dev deployment)
git push origin dev
```

#### **Monitor Dev Deployment**
1. **Go to GitHub Actions**: https://github.com/accelcq/DigitalOceanAIAutomation/actions
2. **Watch the deployment workflow run** for the `dev` branch
3. **Access dev environment**: `http://YOUR_DROPLET_IP:8080`

### **Step 4: Promoting Changes to Production**

#### **Option A: Automatic Merge (No Conflicts)**
```bash
# Switch to main branch
git checkout main

# Pull latest main
git pull origin main

# Merge dev into main
git merge dev

# If no conflicts, push to trigger production deployment
git push origin main
```

#### **Option B: Manual Merge (With Conflicts)**
```bash
# Switch to main branch
git checkout main

# Pull latest main
git pull origin main

# Attempt merge
git merge dev

# If conflicts occur, Git will show:
# CONFLICT (content): Merge conflict in filename.py
# Automatic merge failed; fix conflicts and then commit the result.
```

### **Step 5: Conflict Resolution Process**

#### **When Merge Conflicts Occur:**

1. **Identify Conflicted Files**:
   ```bash
   git status
   # Shows files with conflicts
   ```

2. **Manual Resolution**:
   - Open conflicted files in VS Code
   - Look for conflict markers:
     ```
     <<<<<<< HEAD
     code from main branch
     =======
     code from dev branch
     >>>>>>> dev
     ```
   - **Choose the correct code** or **combine both**
   - **Remove conflict markers** (`<<<<<<<`, `=======`, `>>>>>>>`)

3. **Complete the Merge**:
   ```bash
   # After resolving all conflicts
   git add .
   git commit -m "resolve: Merge dev into main - resolved conflicts in [filename]"
   git push origin main
   ```

4. **Email Notification Process**:
   ```bash
   # If conflicts are complex, send email notification:
   # Subject: "Merge Conflict Resolution Required - DigitalOceanAIAutomation"
   # Recipients: 
   #   - Development Team Lead: dev-lead@accelcq.com
   #   - Project Manager: pm@accelcq.com
   # 
   # Email Content:
   # "Merge conflicts detected in files: [list files]
   #  Manual intervention required for production deployment.
   #  Conflicts resolved in commit: [commit hash]
   #  Production deployment triggered at: [timestamp]"
   ```

### **Step 6: Revert Process (If Needed)**

#### **Revert to Previous Production State**:
```bash
# If production deployment fails after merge
git checkout main

# Find the last working commit
git log --oneline -5

# Revert to previous working commit
git revert HEAD --no-edit

# Push the revert
git push origin main

# Email notification about revert
# Subject: "Production Revert - DigitalOceanAIAutomation"
```

### **Step 7: Environment Verification**

#### **Check Deployment Status**:
```bash
# SSH into droplet
ssh root@YOUR_DROPLET_IP

# Check both containers are running
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"

# Expected output:
# digitaloceanaiautomation-prod  (port 80)  ← Production
# digitaloceanaiautomation-dev   (port 8080) ← Development
```

#### **Access Applications**:
- **Production**: `http://YOUR_DROPLET_IP:80`
- **Development**: `http://YOUR_DROPLET_IP:8080`
- **API Documentation**: 
  - Prod: `http://YOUR_DROPLET_IP:80/docs`
  - Dev: `http://YOUR_DROPLET_IP:8080/docs`

### **Docker Image Impact:**

#### **Registry Structure**:
```
Registry: registry.digitalocean.com/dev-cr/digitaloceanaiautomation
Tags:
├── latest (from main branch - production)
├── dev (from dev branch - development)
└── COMMIT_SHA tags (from both branches)

Droplet Containers:
├── digitaloceanaiautomation-prod (port 80) ← Main branch
└── digitaloceanaiautomation-dev (port 8080) ← Dev branch
```

### **Best Practices**

#### **For Developers**:
1. **Always work on dev branch** for new features
2. **Test in dev environment** before promoting to main
3. **Keep commits small and focused**
4. **Write descriptive commit messages**
5. **Pull latest dev before starting work**

#### **For Deployment**:
1. **Dev deployments are automatic** on push to `dev`
2. **Production deployments are automatic** on push to `main`
3. **Both environments run simultaneously** on same droplet
4. **No downtime** during deployments (containers restart independently)

#### **Conflict Prevention**:
1. **Frequent small merges** to main
2. **Regular communication** between developers
3. **Feature branch naming**: `feature/description` or `fix/description`
4. **Pull latest main** before merging dev

### **Emergency Procedures**

#### **If Production is Down**:
1. **Check GitHub Actions** for deployment status
2. **SSH into droplet** and check container logs:
   ```bash
   docker logs digitaloceanaiautomation-prod
   ```
3. **Quick rollback**:
   ```bash
   git checkout main
   git revert HEAD --no-edit
   git push origin main
   ```
4. **Notify team immediately**

#### **If Dev Environment is Down**:
1. **Check GitHub Actions** for dev deployment status
2. **Restart dev container manually**:
   ```bash
   ssh root@YOUR_DROPLET_IP
   docker restart digitaloceanaiautomation-dev
   ```

### **Email Notification Templates**

#### **Conflict Resolution Email**:
```
Subject: Merge Conflict Resolution - DigitalOceanAIAutomation

Dear Team,

Merge conflicts were detected and resolved during deployment:

Files affected: [list files]
Conflicts resolved in commit: [commit hash]
Resolution time: [timestamp]
Production deployment status: [Success/Failed]

Production URL: http://YOUR_DROPLET_IP:80
Development URL: http://YOUR_DROPLET_IP:8080

Best regards,
[Developer Name]
```

#### **Emergency Revert Email**:
```
Subject: URGENT: Production Revert - DigitalOceanAIAutomation

Dear Team,

Production deployment has been reverted due to critical issues:

Reverted commit: [commit hash]
Revert time: [timestamp]
Current production status: [Status]
Issue description: [Brief description]

Immediate action required: [Next steps]

Production URL: http://YOUR_DROPLET_IP:80

Best regards,
[Developer Name]
```

## Required Information for Deployment

### GitHub Workflow Setup

This project includes automated deployment to DigitalOcean using GitHub Actions. Follow these steps to set up deployment:

### 1. DigitalOcean Prerequisites

#### Container Registry Setup
1. Go to DigitalOcean Control Panel → Container Registry
2. Create a registry named `dev-cr` if it doesn't exist
3. Note the registry URL: `registry.digitalocean.com/dev-cr`

#### Droplet Setup
1. Ensure your droplet `ubuntu-s-1vcpu-1gb-nyc1-01` is running Ubuntu
2. Make sure the droplet has a public IP address
3. Ensure SSH access is enabled

### 2. SSH Key Generation and Setup

#### Generate SSH Key Pair
```bash
# Generate SSH key pair WITHOUT passphrase (recommended for GitHub Actions)
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"

# When prompted for passphrase, press Enter twice (leave empty)
# Enter passphrase (empty for no passphrase): [PRESS ENTER]
# Enter same passphrase again: [PRESS ENTER]

# Alternative: Generate ed25519 key without passphrase
ssh-keygen -t ed25519 -C "your-email@example.com"

# Windows users: If you get "No such file or directory" error, use full path:
# For Windows Command Prompt:
ssh-keygen -t rsa -b 4096 -C "github-actions" -f "C:\Users\%USERNAME%\.ssh\github_actions_key"

# For Windows PowerShell:
ssh-keygen -t rsa -b 4096 -C "github-actions" -f "C:\Users\$env:USERNAME\.ssh\github_actions_key"

# Or navigate to .ssh directory first:
cd C:\Users\%USERNAME%\.ssh
ssh-keygen -t rsa -b 4096 -C "github-actions" -f github_actions_key
```

**Important for GitHub Actions**: Use SSH keys **without passphrases** for automated deployments, as GitHub Actions cannot interactively enter passphrases.

#### Key Identification
- **Private Key**: `~/.ssh/id_rsa` or `C:\Users\USERNAME\.ssh\id_rsa` (Windows) (keep this secret!)
- **Public Key**: `~/.ssh/id_rsa.pub` or `C:\Users\USERNAME\.ssh\id_rsa.pub` (Windows) (safe to share)

#### Add Public Key to DigitalOcean Droplet
```bash
# Linux/Mac - Copy public key content
cat ~/.ssh/id_rsa.pub

# Windows Command Prompt - Copy public key content
type "C:\Users\%USERNAME%\.ssh\github_actions_key.pub"

# Windows PowerShell - Copy public key content
Get-Content "C:\Users\$env:USERNAME\.ssh\github_actions_key.pub"

# SSH into your droplet and add the public key
ssh root@YOUR_DROPLET_IP
mkdir -p ~/.ssh
echo "PASTE_PUBLIC_KEY_CONTENT_HERE" >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
exit
```

### 3. Required GitHub Secrets

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

#### DIGITALOCEAN_ACCESS_TOKEN
- **Value**: Your DigitalOcean API token
- **How to get**: 
  1. Go to DigitalOcean Control Panel → API
  2. Click "Generate New Token"
  3. Name it (e.g., "GitHub Actions")
  4. Select "Read" and "Write" scopes
  5. Copy the generated token

#### DROPLET_HOST
- **Value**: Your droplet's public IP address
- **How to get**: DigitalOcean Control Panel → Droplets → Copy IP address

#### DROPLET_USERNAME
- **Value**: `root` (or your custom user if you created one)

#### DROPLET_SSH_KEY
- **Value**: Contents of your **private key** file **without passphrase**
- **How to get**:
  ```bash
  # Linux/Mac - If using existing key WITHOUT passphrase
  cat ~/.ssh/id_rsa
  
  # Windows Command Prompt - Display private key
  type "C:\Users\%USERNAME%\.ssh\github_actions_key"
  
  # Windows PowerShell - Display private key
  Get-Content "C:\Users\$env:USERNAME\.ssh\github_actions_key"
  
  # If your current key has a passphrase, create new one without passphrase
  # Linux/Mac:
  ssh-keygen -t rsa -b 4096 -C "github-actions@example.com" -f ~/.ssh/github_actions_key
  
  # Windows Command Prompt:
  ssh-keygen -t rsa -b 4096 -C "github-actions@example.com" -f "C:\Users\%USERNAME%\.ssh\github_actions_key"
  
  # Windows PowerShell:
  ssh-keygen -t rsa -b 4096 -C "github-actions@example.com" -f "C:\Users\$env:USERNAME\.ssh\github_actions_key"
  
  # Press Enter twice when prompted for passphrase (leave empty)
  ```
- **Important**: Copy the entire content including:
  ```
  -----BEGIN OPENSSH PRIVATE KEY-----
  [key content]
  -----END OPENSSH PRIVATE KEY-----
  ```

**Note**: If you create a new key for GitHub Actions, remember to add the corresponding public key to your droplet's `~/.ssh/authorized_keys` file.

### 4. Adding Secrets to GitHub Repository

1. Navigate to your GitHub repository
2. Go to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add each secret:
   - Name: `DIGITALOCEAN_ACCESS_TOKEN`, Value: [your DO token]
   - Name: `DROPLET_HOST`, Value: [your droplet IP]
   - Name: `DROPLET_USERNAME`, Value: `root`
   - Name: `DROPLET_SSH_KEY`, Value: [your private key content]

### 5. Workflow Behavior

The GitHub Action will automatically:
- **Trigger**: On every push to `main` branch
- **Cleanup**: Automatically clean up existing repositories to avoid DigitalOcean registry limits
- **Build**: Docker image using the Dockerfile
- **Push**: Image to DigitalOcean Container Registry `dev-cr`
- **Deploy**: Pull and run the container on your droplet
- **Access**: Application will be available at `http://YOUR_DROPLET_IP`

**Note**: The workflow includes a "Clean up existing repository before build" step that automatically resolves repository limit issues by cleaning up old repositories or manifests before pushing new images.

### 6. Manual Deployment Commands

If you need to deploy manually:

```bash
# Build and push to registry
docker build -t registry.digitalocean.com/dev-cr/digitaloceanaiautomation:latest .
doctl registry login
docker push registry.digitalocean.com/dev-cr/digitaloceanaiautomation:latest

# Deploy on droplet
ssh root@YOUR_DROPLET_IP
docker pull registry.digitalocean.com/dev-cr/digitaloceanaiautomation:latest
docker stop digitaloceanaiautomation || true
docker rm digitaloceanaiautomation || true
docker run -d --name digitaloceanaiautomation -p 80:8000 --restart unless-stopped registry.digitalocean.com/dev-cr/digitaloceanaiautomation:latest
```

### 7. Troubleshooting

#### Common Issues:
- **SSH Connection Failed**: Verify droplet IP, username, and private key
- **SSH Passphrase Required**: Use SSH keys without passphrases for GitHub Actions
- **Registry Login Failed**: Check DigitalOcean access token permissions
- **Container Not Starting**: Check application logs with `docker logs digitaloceanaiautomation`
- **Port 80 Access Issues**: Ensure droplet firewall allows HTTP traffic
- **Registry Repository Limit**: Basic plan allows only 1 repository

#### SSH Key Issues:
If you encounter SSH passphrase prompts during deployment:

**Option 1: Create new SSH key without passphrase (Recommended)**
```bash
# Linux/Mac - Create dedicated key for GitHub Actions
ssh-keygen -t rsa -b 4096 -C "github-actions" -f ~/.ssh/github_actions_key

# Windows Command Prompt - Create dedicated key for GitHub Actions
ssh-keygen -t rsa -b 4096 -C "github-actions" -f "C:\Users\%USERNAME%\.ssh\github_actions_key"

# Windows PowerShell - Create dedicated key for GitHub Actions
ssh-keygen -t rsa -b 4096 -C "github-actions" -f "C:\Users\$env:USERNAME\.ssh\github_actions_key"

# Press Enter twice for empty passphrase

# Linux/Mac - Add public key to droplet
cat ~/.ssh/github_actions_key.pub

# Windows Command Prompt - Add public key to droplet
type "C:\Users\%USERNAME%\.ssh\github_actions_key.pub"

# Windows PowerShell - Add public key to droplet
Get-Content "C:\Users\$env:USERNAME\.ssh\github_actions_key.pub"

# Copy this and add to droplet's ~/.ssh/authorized_keys

# Linux/Mac - Use private key content in GitHub secret
cat ~/.ssh/github_actions_key

# Windows Command Prompt - Use private key content in GitHub secret
type "C:\Users\%USERNAME%\.ssh\github_actions_key"

# Windows PowerShell - Use private key content in GitHub secret
Get-Content "C:\Users\$env:USERNAME\.ssh\github_actions_key"
```

**Option 2: Remove passphrase from existing key**
```bash
# Remove passphrase from existing key
ssh-keygen -p -f ~/.ssh/id_rsa
# Enter old passphrase, then press Enter twice for new empty passphrase
```

**Option 3: Use SSH agent (Advanced)**
- Set up SSH agent forwarding (more complex setup)

#### Container Registry Repository Limit Fix:
**Note**: DigitalOcean free tier has a limit of 1 repository. The deployment workflow automatically handles this by:
1. **Reusing the same repository** - Deletes old tags/images instead of creating new repositories
2. **Running garbage collection** - Frees up storage space after cleanup
3. **Waiting for cleanup completion** - Ensures cleanup finishes before pushing new images

If you still encounter "registry contains 1 repositories, limit is 1" error, try these manual solutions:

**Option 1: Delete existing tags (Recommended for Free Tier)**
```bash
# List existing repositories
doctl registry repository list-v2 dev-cr

# List tags in your repository
doctl registry repository list-tags dev-cr digitaloceanaiautomation

# Delete specific tags
doctl registry repository delete-tag dev-cr digitaloceanaiautomation TAG_NAME --force

# Or delete all tags in the repository (keeps repository, removes content)
doctl registry repository list-tags dev-cr digitaloceanaiautomation --format Tag --no-header | xargs -I {} doctl registry repository delete-tag dev-cr digitaloceanaiautomation {} --force

# Run garbage collection to free space
doctl registry garbage-collection start dev-cr
```

**Option 2: Delete entire repository (Manual)**
```bash
# List existing repositories
doctl registry repository list-v2 dev-cr

# Delete unwanted repository
doctl registry repository delete dev-cr REPOSITORY_NAME --force

# Or delete all manifests in a repository
doctl registry repository delete-manifest dev-cr REPOSITORY_NAME --force
```

**Option 2: Upgrade registry plan**
- Go to DigitalOcean Control Panel → Container Registry
- Click "Settings" → "Upgrade Plan"
- Choose a plan with more repository limits

**Option 3: Use different registry name**
- Create a new registry with a different name
- Update the workflow `REGISTRY` environment variable

#### Checking Deployment Status:
```bash
# SSH into droplet and check container status
ssh root@YOUR_DROPLET_IP
docker ps
docker logs digitaloceanaiautomation
```