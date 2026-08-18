## EC2 Deployment

The app runs as a `systemd` service on EC2. Use the steps below to deploy or update it via AWS Systems Manager (SSM) Session Manager — no SSH key needed.

### First-time setup

```bash
# 1. Connect via SSM Session Manager (AWS Console → EC2 → Connect → Session Manager)
bash
cd ~/Projects/genai-dashboard

# 2. Download the deployment package from S3
aws s3 cp s3://dhruv-ai-lab-general-purpose-bucket-4-eu-west-1-an/genai-dashboard/genai-dashboard-deploy.zip .

# 3. Extract (overwrites existing files)
unzip -o genai-dashboard-deploy.zip

# 4. Edit .env with your S3 bucket and AWS settings (created from env.example on first extract)
nano .env

# 5. Install dependencies (first time only)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Start the service
sudo systemctl restart genai-dashboard
sudo systemctl status genai-dashboard   # verify it's running
```

### Updating to a new version

```bash
bash
cd ~/Projects/genai-dashboard
aws s3 cp s3://dhruv-ai-lab-general-purpose-bucket-44-eu-west-1-an/genai-dashboard/genai-dashboard-deploy.zip .
unzip -o genai-dashboard-deploy.zip
sudo systemctl restart genai-dashboard
```

> **Note:** `unzip -o` overwrites all files including `.env`. Back up your `.env` first if you have local changes:
> ```bash
> cp .env .env.backup
> unzip -o genai-dashboard-deploy.zip
> # restore any custom values if needed
> ```

### systemd service

The app is managed by `systemd`. Common commands:

```bash
sudo systemctl start genai-dashboard      # start
sudo systemctl stop genai-dashboard       # stop
sudo systemctl restart genai-dashboard    # restart
sudo systemctl status genai-dashboard     # check status / recent logs
sudo journalctl -u genai-dashboard -f     # tail live logs
```

The dashboard is available at `http://<EC2-private-IP>:8501` (or via a load balancer / CloudFront if configured).

---

## Deployment Package

A pre-built zip (`genai-dashboard-deploy.zip`) is stored in S3 for easy sharing and deployment:

| | |
|---|---|
| **Bucket** | `dhruv-ai-lab-general-purpose-bucket-4-eu-west-1-an` |
| **Region** | `eu-west-1` |
| **S3 Key** | `genai-dashboard/genai-dashboard-deploy.zip` |

### Download via AWS CLI

```bash
aws s3 cp s3://dhruv-ai-lab-general-purpose-bucket-4-eu-west-1-an/genai-dashboard/genai-dashboard-deploy.zip .
```

### Upload a new version

```bash
# From inside the ai-chromadb-poc folder:
Compress-Archive -Path * -DestinationPath genai-dashboard-deploy.zip -Force   # Windows PowerShell
# zip -r genai-dashboard-deploy.zip . --exclude "*.pyc" "__pycache__/*" ".venv/*" "venv/*"  # Linux/macOS

aws s3 cp genai-dashboard-deploy.zip s3://dhruv-ai-lab-general-purpose-bucket-4-eu-west-1-an/genai-dashboard/genai-dashboard-deploy.zip
```

After downloading, unzip and follow the **Quick Start** steps above.

---

## Support

- Verify Bedrock is working: AWS Console → Bedrock → Playgrounds → Chat → select Claude model
- Enable verbose logging: `streamlit run app.py --logger.level debug`
- IAM policy issues: use AWS Policy Simulator to test `s3:GetObject` and `bedrock:InvokeModel`

---

## AWS EC2 Deployment

### Prerequisites

- EC2 instance (Amazon Linux 2023 or Ubuntu) with an IAM role granting `s3:GetObject` / `s3:ListBucket` on your CSV bucket and `bedrock:InvokeModel` on your Claude model
- S3 bucket to stage the deployment zip
- Security group inbound rules: **HTTPS — port 443** and **HTTP — port 80** open to your IP (or `0.0.0.0/0`). Port 8002 must **not** be open — traffic goes through Nginx only.

---

### 1. Build the deployment zip (local)

```powershell
Compress-Archive -Path * -DestinationPath genai-dashboard-deploy.zip -Force
```

Exclude `.venv/`, `.git/`, `__pycache__/`, and `.env` before zipping (or remove them from the archive afterwards).

### 2. Upload to S3 (local)

```bash
aws s3 cp genai-dashboard-deploy.zip s3://<YOUR_BUCKET>/genai-dashboard/ --profile <YOUR_PROFILE>
```

---

### 3. Server setup (EC2 — run once)

```bash
# Amazon Linux 2023
sudo dnf update -y
sudo dnf install unzip -y

# Ubuntu alternative
# sudo apt-get update && sudo apt-get install unzip -y
```

### 4. Download and extract

```bash
mkdir -p ~/projects && cd ~/projects
aws s3 cp s3://<YOUR_BUCKET>/genai-dashboard/genai-dashboard-deploy.zip .
unzip genai-dashboard-deploy.zip -d genai-dashboard
cd genai-dashboard
```

### 5. Create virtual environment, install dependencies, and configure

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp env.example .env
# edit .env with your S3_BUCKET, S3_KEY, AWS_REGION, BEDROCK_REGION, etc.
```

> AWS credentials come from the EC2 IAM role automatically — leave `AWS_PROFILE` blank in `.env`.

### 6. Create systemd service

Paste this **directly** into the terminal (no markdown fences):

```
sudo tee /etc/systemd/system/genai-dashboard.service > /dev/null <<'EOF'
[Unit]
Description=RAKBANK GenAI Cost Dashboard
After=network.target

[Service]
Type=simple
User=ssm-user
WorkingDirectory=/home/ssm-user/Projects/genai-dashboard
Environment="PATH=/home/ssm-user/Projects/genai-dashboard/.venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/home/ssm-user/Projects/genai-dashboard/.venv/bin/streamlit run app.py --server.port 8003 --server.address 0.0.0.0 --server.headless true
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
```

Verify the file was written:

```
cat /etc/systemd/system/genai-dashboard.service
```

### 7. Enable and start

```bash
sudo systemctl daemon-reload
sudo systemctl enable genai-dashboard
sudo systemctl start genai-dashboard
sudo systemctl status genai-dashboard
sudo systemctl restart genai-dashboard
```

App is now available at `http://127.0.0.1:8002` (localhost only — not exposed to the internet).

---

### 8. Set up Nginx as HTTPS reverse proxy (run once on EC2)

Nginx sits in front of Streamlit and terminates SSL on port 443, forwarding traffic to the app on `127.0.0.1:8002`.

```
Browser (HTTPS :443) → [Nginx] → [Streamlit :8002 localhost]
```

**Install Nginx:**
```bash
sudo yum install -y nginx          # Amazon Linux 2023
```

**Generate a self-signed SSL certificate:**
```bash
sudo mkdir -p /etc/nginx/ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/dashboard.key \
  -out /etc/nginx/ssl/dashboard.crt \
  -subj "/CN=<EC2_PRIVATE_IP>"
```

**Write the Nginx config:**

```bash
sudo tee /etc/nginx/conf.d/genai-dashboard.conf > /dev/null <<'EOF'
server {
    listen 443 ssl;
    ssl_certificate     /etc/nginx/ssl/dashboard.crt;
    ssl_certificate_key /etc/nginx/ssl/dashboard.key;

    location / {
        proxy_pass http://127.0.0.1:8002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
server {
    listen 80;
    return 301 https://$host$request_uri;
}
EOF
```

> Streamlit uses WebSockets, so the `Upgrade`/`Connection` headers above are required for the UI to work behind the proxy.
> On Amazon Linux, Nginx auto-loads all `*.conf` files from `/etc/nginx/conf.d/` — no symlinks needed.

**Test and enable:**
```bash
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx
```

**Verify:**
```bash
# Nginx listening on 443 and 80
sudo ss -tlnp | grep nginx

# App responds via HTTPS locally
curl -k https://127.0.0.1/
```

App is now available at `https://<EC2_PUBLIC_IP>` (browser will show a self-signed cert warning — click **Advanced → Proceed**).

---

### Service management

```bash
sudo systemctl restart genai-dashboard
sudo systemctl stop genai-dashboard

# Live logs
sudo journalctl -u genai-dashboard -f

# Last 50 lines
sudo journalctl -u genai-dashboard -n 50 --no-pager
```

---

### Updating the application

```bash
# Local — rebuild and upload
Compress-Archive -Path * -DestinationPath genai-dashboard-deploy.zip -Force
aws s3 cp genai-dashboard-deploy.zip s3://<YOUR_BUCKET>/genai-dashboard/ --profile <YOUR_PROFILE>
