# 🚀 Deployment Guide

## Deployment Options

This guide covers various deployment strategies for the Adobe Hackathon PDF Intelligence toolkit.

---

## 🐳 Docker Deployment (Recommended)

### Web Interface Deployment

#### Build Image
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/adobe-hackathon-pdf-intelligence.git
cd adobe-hackathon-pdf-intelligence

# Build web application image
docker build -t pdf-intelligence-web .
```

#### Run Container
```bash
# Run with port mapping
docker run -d \
  --name pdf-intelligence \
  -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/results:/app/results \
  pdf-intelligence-web

# Access at http://localhost:5000
```

#### Production Configuration
```bash
# Run with environment variables
docker run -d \
  --name pdf-intelligence-prod \
  -p 80:5000 \
  -e FLASK_ENV=production \
  -e MODEL_PATH=/app/models/all-MiniLM-L6-v2 \
  -e TOKENIZERS_PARALLELISM=false \
  -e MAX_WORKERS=4 \
  --restart unless-stopped \
  pdf-intelligence-web
```

### Command Line Deployment

#### Build CLI Image
```bash
docker build -f Dockerfile.main -t pdf-intelligence-cli .
```

#### Run Batch Processing
```bash
# Process PDFs in input directory
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  pdf-intelligence-cli python main2.py

# Run Challenge 1B
docker run --rm \
  -v $(pwd)/Challenge_1b:/app/Challenge_1b \
  -v $(pwd)/output:/app/output \
  pdf-intelligence-cli python main.py
```

---

## ☁️ Cloud Deployment

### AWS EC2 Deployment

#### 1. Launch EC2 Instance
```bash
# Launch Ubuntu 20.04 LTS instance
# Instance type: t3.medium or larger (4GB+ RAM recommended)
# Security group: Allow HTTP (80) and SSH (22)
```

#### 2. Setup Instance
```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Git
sudo apt install git -y
```

#### 3. Deploy Application
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/adobe-hackathon-pdf-intelligence.git
cd adobe-hackathon-pdf-intelligence

# Build and run
docker build -t pdf-intelligence .
docker run -d \
  --name pdf-intelligence \
  -p 80:5000 \
  --restart unless-stopped \
  pdf-intelligence
```

#### 4. Configure Domain (Optional)
```bash
# Install nginx for reverse proxy
sudo apt install nginx -y

# Configure nginx
sudo nano /etc/nginx/sites-available/pdf-intelligence
```

Nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/pdf-intelligence /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Google Cloud Platform (GCP)

#### Cloud Run Deployment
```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/pdf-intelligence

# Deploy to Cloud Run
gcloud run deploy pdf-intelligence \
  --image gcr.io/PROJECT_ID/pdf-intelligence \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 900
```

### Azure Container Instances

```bash
# Create resource group
az group create --name pdf-intelligence-rg --location eastus

# Deploy container
az container create \
  --resource-group pdf-intelligence-rg \
  --name pdf-intelligence \
  --image your-registry/pdf-intelligence:latest \
  --dns-name-label pdf-intelligence-app \
  --ports 5000 \
  --memory 4 \
  --cpu 2
```

---

## 🖥️ VPS/Server Deployment

### Ubuntu/Debian Server

#### 1. System Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv git -y
sudo apt install build-essential poppler-utils tesseract-ocr -y
```

#### 2. Application Setup
```bash
# Create application user
sudo useradd -m -s /bin/bash pdfapp
sudo su - pdfapp

# Clone and setup
git clone https://github.com/YOUR_USERNAME/adobe-hackathon-pdf-intelligence.git
cd adobe-hackathon-pdf-intelligence

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. Service Configuration
Create systemd service file:
```bash
sudo nano /etc/systemd/system/pdf-intelligence.service
```

Service configuration:
```ini
[Unit]
Description=PDF Intelligence Web Application
After=network.target

[Service]
Type=simple
User=pdfapp
WorkingDirectory=/home/pdfapp/adobe-hackathon-pdf-intelligence
Environment=PATH=/home/pdfapp/adobe-hackathon-pdf-intelligence/venv/bin
ExecStart=/home/pdfapp/adobe-hackathon-pdf-intelligence/venv/bin/python web_app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 4. Start Service
```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable pdf-intelligence
sudo systemctl start pdf-intelligence

# Check status
sudo systemctl status pdf-intelligence
```

---

## 🔧 Production Configuration

### Environment Variables
```bash
# Production settings
export FLASK_ENV=production
export FLASK_DEBUG=False
export MODEL_PATH=/app/models/all-MiniLM-L6-v2
export TOKENIZERS_PARALLELISM=false
export MAX_WORKERS=4
export OCR_ENABLED=1
```

### Performance Tuning
```python
# web_app.py production settings
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True,
        processes=1
    )
```

### Security Hardening
```python
# Add security headers
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app, force_https=False)  # Set True for HTTPS

# Configure file upload limits
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
```

---

## 📊 Monitoring & Logging

### Application Logging
```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
if not app.debug:
    file_handler = RotatingFileHandler(
        'logs/pdf-intelligence.log', 
        maxBytes=10240000, 
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### Health Monitoring
```bash
# Simple health check script
#!/bin/bash
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/health)
if [ $response -eq 200 ]; then
    echo "Service is healthy"
else
    echo "Service is down"
    # Restart service
    sudo systemctl restart pdf-intelligence
fi
```

### Resource Monitoring
```bash
# Monitor resource usage
docker stats pdf-intelligence

# Check logs
docker logs pdf-intelligence -f
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Build Docker image
      run: docker build -t pdf-intelligence .
    
    - name: Deploy to server
      run: |
        # Add deployment commands here
        echo "Deploying to production..."
```

---

## 🛡️ Security Considerations

### Production Security Checklist
- [ ] Use HTTPS in production
- [ ] Implement rate limiting
- [ ] Add authentication if needed
- [ ] Validate all inputs
- [ ] Use environment variables for secrets
- [ ] Regular security updates
- [ ] Monitor for vulnerabilities
- [ ] Backup important data

### Firewall Configuration
```bash
# Ubuntu UFW firewall
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancer (nginx, HAProxy)
- Deploy multiple container instances
- Implement session management
- Use external file storage

### Vertical Scaling
- Increase CPU/memory allocation
- Optimize multiprocessing settings
- Use faster storage (SSD)
- Tune application parameters

### Performance Optimization
- Enable caching for static files
- Compress responses
- Optimize AI model loading
- Use CDN for static assets

---

## 🔧 Troubleshooting

### Common Issues

#### Container Won't Start
```bash
# Check logs
docker logs pdf-intelligence

# Check resource usage
docker system df
```

#### Out of Memory
```bash
# Increase container memory
docker run -m 4g pdf-intelligence

# Monitor memory usage
docker stats
```

#### Slow Processing
- Check CPU usage
- Verify model loading
- Optimize multiprocessing settings
- Consider GPU acceleration

#### File Upload Issues
- Check file size limits
- Verify disk space
- Check permissions
- Review nginx/proxy settings

For additional support, check the [API Documentation](API_DOCUMENTATION.md) and [Contributing Guide](CONTRIBUTING.md).
