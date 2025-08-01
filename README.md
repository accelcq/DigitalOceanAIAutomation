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
# Generate SSH key pair (run this on your local machine)
ssh-keygen -t rsa -b 4096 -c "your-email@example.com"

# When prompted, save to default location: ~/.ssh/id_rsa
# Set a passphrase or leave empty for no passphrase
```

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
- **Value**: Contents of your **private key** file
- **How to get**:
  ```bash
  # Display private key content (copy this entire output)
  cat ~/.ssh/id_rsa
  ```
- **Important**: Copy the entire content including:
  ```
  -----BEGIN OPENSSH PRIVATE KEY-----
  [key content]
  -----END OPENSSH PRIVATE KEY-----
  ```

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
- **Registry Login Failed**: Check DigitalOcean access token permissions
- **Container Not Starting**: Check application logs with `docker logs digitaloceanaiautomation`
- **Port 80 Access Issues**: Ensure droplet firewall allows HTTP traffic
- **Registry Repository Limit**: Basic plan allows only 1 repository

#### Container Registry Repository Limit Fix:
**Note**: The deployment workflow now automatically handles repository cleanup, but if you need to manually resolve "registry contains 1 repositories, limit is 1" error:

**Option 1: Delete existing repositories (Manual)**
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