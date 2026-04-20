# Deployment Guide for LLM Tutor

This guide covers deploying LLM Tutor to various platforms.

## Table of Contents
1. [Streamlit Cloud (Easiest)](#streamlit-cloud)
2. [Heroku](#heroku)
3. [AWS](#aws)
4. [Google Cloud Platform](#google-cloud-platform)
5. [Azure](#azure)
6. [Docker (Local or Server)](#docker)
7. [Self-Hosted VPS](#self-hosted-vps)

---

## Streamlit Cloud (Easiest)

### Prerequisites
- GitHub account with the repository
- Streamlit Cloud account (free tier available)
- GROQ API key

### Steps

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"

3. **Configure Deployment**
   - Select your repository
   - Branch: select `main`
   - Main file path: `capstone_streamlit.py`

4. **Set Environment Variables**
   - Click "Advanced settings"
   - Under "Secrets", paste:
   ```toml
   GROQ_API_KEY = "gsk_your_api_key_here"
   ```

5. **Deploy**
   - Click "Deploy"
   - App will be live in ~5 minutes

### URL Format
```
https://<username>-llm-tutor.streamlit.app
```

### Notes
- Free tier has resource limits
- Paid tier for production use: $5-100+/month
- Storage: 1GB (community tier)
- Always use Streamlit secrets, NOT .env files

---

## Heroku

### Prerequisites
- Heroku CLI installed
- GitHub repository
- GROQ API key

### Steps

1. **Create Heroku App**
   ```bash
   heroku login
   heroku create your-llm-tutor-app
   ```

2. **Add Buildpack**
   ```bash
   heroku buildpacks:add heroku/python
   ```

3. **Create Procfile**
   ```bash
   echo "web: streamlit run capstone_streamlit.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set GROQ_API_KEY="gsk_your_api_key_here"
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **View Logs**
   ```bash
   heroku logs --tail
   ```

### URL Format
```
https://your-llm-tutor-app.herokuapp.com
```

### Notes
- Free tier discontinued as of Nov 2022
- Paid dyno: $7+/month
- Need to include `Procfile` in repo

---

## AWS (Elastic Beanstalk)

### Prerequisites
- AWS account
- AWS CLI configured
- GROQ API key

### Steps

1. **Initialize EB**
   ```bash
   eb init -p python-3.11 llm-tutor --region us-east-1
   ```

2. **Create Procfile**
   ```
   web: streamlit run capstone_streamlit.py --server.port=8000
   ```

3. **Create .ebextensions/python.config**
   ```yaml
   option_settings:
     aws:elasticbeanstalk:application:environment:
       GROQ_API_KEY: your_api_key_here
   ```

4. **Deploy**
   ```bash
   eb create llm-tutor-env
   eb deploy
   ```

5. **View App**
   ```bash
   eb open
   ```

### Cost
- ~$5-20/month for small workloads
- Auto-scaling available

---

## Google Cloud Platform (Cloud Run)

### Prerequisites
- GCP account
- Docker installed
- gcloud CLI installed

### Steps

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD streamlit run capstone_streamlit.py
   ```

2. **Build & Push Image**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/llm-tutor
   ```

3. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy llm-tutor \
     --image gcr.io/PROJECT_ID/llm-tutor \
     --set-env-vars GROQ_API_KEY=gsk_your_key \
     --memory 1Gi \
     --region us-central1
   ```

### Cost
- Free tier: 2 million requests/month
- After free tier: $0.40 per million requests

---

## Azure (App Service)

### Prerequisites
- Azure account
- Azure CLI installed
- Docker installed

### Steps

1. **Create Azure App Service**
   ```bash
   az group create --name llm-tutor-rg --location "West US"
   az appservice plan create --name llm-tutor-plan --resource-group llm-tutor-rg --sku B1 --is-linux
   ```

2. **Create Web App**
   ```bash
   az webapp create --resource-group llm-tutor-rg --plan llm-tutor-plan --name llm-tutor-app --runtime "python|3.11"
   ```

3. **Configure Deployment**
   ```bash
   az webapp config appsettings set --resource-group llm-tutor-rg --name llm-tutor-app \
     --settings GROQ_API_KEY="gsk_your_key"
   ```

4. **Deploy from Git**
   ```bash
   az webapp up --name llm-tutor-app --resource-group llm-tutor-rg
   ```

### Cost
- Free tier: Limited resources
- Basic plan: $12+/month

---

## Docker (Local or Server)

### Build & Run Locally

1. **Create Dockerfile** (or use existing)
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8501
   CMD streamlit run capstone_streamlit.py --server.port=8501
   ```

2. **Build Image**
   ```bash
   docker build -t llm-tutor:latest .
   ```

3. **Run Locally**
   ```bash
   docker run -p 8501:8501 \
     -e GROQ_API_KEY=gsk_your_key \
     llm-tutor:latest
   ```

4. **Access App**
   ```
   http://localhost:8501
   ```

### Push to Docker Hub

1. **Tag Image**
   ```bash
   docker tag llm-tutor:latest yourusername/llm-tutor:latest
   ```

2. **Login to Docker Hub**
   ```bash
   docker login
   ```

3. **Push**
   ```bash
   docker push yourusername/llm-tutor:latest
   ```

### Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      GROQ_API_KEY: ${GROQ_API_KEY}
    volumes:
      - ./memory_state:/app/memory_state
```

Run with:
```bash
docker-compose up
```

---

## Self-Hosted VPS

### Prerequisites
- VPS (DigitalOcean, Linode, AWS EC2, etc.)
- SSH access
- Domain name (optional)

### Steps

1. **SSH into Server**
   ```bash
   ssh root@your_vps_ip
   ```

2. **Update System**
   ```bash
   apt update && apt upgrade -y
   ```

3. **Install Python & Dependencies**
   ```bash
   apt install python3.11 python3-pip python3-venv nginx -y
   ```

4. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/llm-tutor.git
   cd llm-tutor
   ```

5. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Create .env File**
   ```bash
   echo 'GROQ_API_KEY=gsk_your_key' > .env
   chmod 600 .env
   ```

7. **Set Up Systemd Service**
   ```bash
   sudo tee /etc/systemd/system/llm-tutor.service > /dev/null <<EOF
   [Unit]
   Description=LLM Tutor Application
   After=network.target

   [Service]
   Type=simple
   User=root
   WorkingDirectory=/root/llm-tutor
   Environment="PATH=/root/llm-tutor/venv/bin"
   ExecStart=/root/llm-tutor/venv/bin/streamlit run capstone_streamlit.py --server.port=8501
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   EOF
   ```

8. **Start Service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start llm-tutor
   sudo systemctl enable llm-tutor
   ```

9. **Configure Nginx (Reverse Proxy)**
   ```bash
   sudo tee /etc/nginx/sites-available/llm-tutor > /dev/null <<EOF
   server {
       listen 80;
       server_name your_domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade \$http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host \$host;
           proxy_cache_bypass \$http_upgrade;
       }
   }
   EOF
   ```

10. **Enable Nginx Site**
    ```bash
    sudo ln -s /etc/nginx/sites-available/llm-tutor /etc/nginx/sites-enabled/
    sudo systemctl restart nginx
    ```

11. **Set Up SSL (Let's Encrypt)**
    ```bash
    apt install certbot python3-certbot-nginx -y
    certbot --nginx -d your_domain.com
    ```

### Cost
- DigitalOcean: $4-6+/month
- Linode: $5+/month
- AWS EC2: Pay-as-you-go

### Monitoring
```bash
sudo systemctl status llm-tutor
sudo journalctl -f -u llm-tutor
```

---

## Comparison Table

| Platform | Cost | Setup Time | Ease | Free Tier | Best For |
|----------|------|------------|------|-----------|----------|
| Streamlit Cloud | $5-100/mo | 5 min | ⭐⭐⭐⭐⭐ | Yes (limited) | Quick demos, prototyping |
| Heroku | $7+/mo | 10 min | ⭐⭐⭐⭐ | No | Small projects |
| AWS EB | $5-20/mo | 15 min | ⭐⭐⭐ | Limited | Scalable apps |
| GCP Cloud Run | $0.40/M req | 10 min | ⭐⭐⭐⭐ | Yes (2M/mo) | Event-driven apps |
| Azure | $12+/mo | 15 min | ⭐⭐⭐ | Limited | Enterprise |
| Docker + VPS | $4+/mo | 20 min | ⭐⭐⭐ | No | Full control |

---

## Security Checklist

- [ ] API keys in environment variables, NOT in code
- [ ] HTTPS/SSL enabled
- [ ] Rate limiting configured
- [ ] Monitoring & logging enabled
- [ ] Backups configured
- [ ] Only necessary ports open
- [ ] Regular security updates

---

## Monitoring & Logs

### Streamlit Cloud
- Built-in dashboard at streamlit.io

### Docker/VPS
```bash
# View logs
docker logs <container-id>

# Monitor resources
docker stats <container-id>
```

### Health Checks
```bash
curl -I https://your_domain.com
```

---

## Rollback & Updates

### Streamlit Cloud
- Automatic (just push to main)

### Docker
```bash
# Push new version
docker tag llm-tutor:latest yourusername/llm-tutor:v1.1.0
docker push yourusername/llm-tutor:v1.1.0

# Rollback
docker run yourusername/llm-tutor:v1.0.0
```

---

## Support

- 📧 Issues: https://github.com/yourusername/llm-tutor/issues
- 📖 Docs: Check [README.md](README.md) and [CONFIG.md](CONFIG.md)
- 💬 Discussions: GitHub Discussions

---

**Last Updated**: 2026-04-20
**Version**: 1.0.0
