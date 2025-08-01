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
```

**Important for GitHub Actions**: Use SSH keys **without passphrases** for automated deployments, as GitHub Actions cannot interactively enter passphrases.

#### Key Identification
- **Private Key**: `~/.ssh/id_rsa` (keep this secret!)
- **Public Key**: `~/.ssh/id_rsa.pub` (safe to share)

#### Add Public Key to DigitalOcean Droplet
```bash
# Copy public key content
cat ~/.ssh/id_rsa.pub

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
  # If using existing key WITHOUT passphrase
  cat ~/.ssh/id_rsa
  
  # If your current key has a passphrase, create new one without passphrase
  ssh-keygen -t rsa -b 4096 -C "github-actions@example.com" -f ~/.ssh/github_actions_key
  # Press Enter twice when prompted for passphrase (leave empty)
  
  # Then display the new private key
  cat ~/.ssh/github_actions_key
  ```
- **Important**: Copy the entire content including:
  ```
  -----BEGIN OPENSSH PRIVATE KEY-----
  [key content]
  -----END OPENSSH PRIVATE KEY-----
  ```

**Note**: If you create a new key for GitHub Actions, remember to add the corresponding public key (`~/.ssh/github_actions_key.pub`) to your droplet's `~/.ssh/authorized_keys` file.

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
# Create dedicated key for GitHub Actions
ssh-keygen -t rsa -b 4096 -C "github-actions" -f ~/.ssh/github_actions_key
# Press Enter twice for empty passphrase

# Add public key to droplet
cat ~/.ssh/github_actions_key.pub
# Copy this and add to droplet's ~/.ssh/authorized_keys

# Use private key content in GitHub secret
cat ~/.ssh/github_actions_key
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