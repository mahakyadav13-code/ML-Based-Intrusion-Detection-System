# 🚀 Deployment Guide - ML-Based Intrusion Detection System

Complete guide for deploying the IDS Flask application to various environments.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Production Checklist](#production-checklist)
6. [Monitoring & Maintenance](#monitoring--maintenance)

---

## 🔧 Prerequisites

### Required Software
- **Python**: 3.11 or higher
- **Docker**: 20.10+ (for containerized deployment)
- **Docker Compose**: 1.29+ (optional)
- **Git**: For version control

### System Requirements
- **CPU**: 2+ cores recommended
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 10GB free space
- **OS**: Windows 10/11, Linux (Ubuntu 20.04+), macOS 11+

---

## 💻 Local Development

### Method 1: Direct Python Execution

```powershell
# 1. Clone repository
git clone <repository-url>
cd "Internship Project 1"

# 2. Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate    # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate sample data (if needed)
python scripts\generate_sample_data.py

# 5. Train models (if not already trained)
python src\data_preprocessing.py
python src\train_model.py
python src\evaluate_model.py

# 6. Run Flask application
python flask_app.py
```

**Access**: http://localhost:5000

### Method 2: Using Launch Script

```powershell
.\RUN_FLASK.ps1
```

---

## 🐳 Docker Deployment

### Quick Start with Docker

```bash
# Build Docker image
docker build -t ids-flask-app .

# Run container
docker run -d \
  --name ids-app \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  ids-flask-app
```

**Access**: http://localhost:5000

### Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f ids-app

# Stop services
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

### Docker Compose with Nginx

```yaml
# Full stack with reverse proxy
docker-compose up -d
```

This includes:
- Flask application on port 5000
- Nginx reverse proxy on port 80/443
- Automatic SSL/TLS (configure certificates)

---

## ☁️ Cloud Deployment

### AWS Deployment

#### Option 1: AWS EC2

```bash
# 1. Launch EC2 instance (Amazon Linux 2 or Ubuntu)
# Instance type: t2.medium or larger

# 2. Connect via SSH
ssh -i your-key.pem ec2-user@<instance-ip>

# 3. Install Docker
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# 4. Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 5. Clone and deploy
git clone <your-repo>
cd "Internship Project 1"
docker-compose up -d

# 6. Configure security group
# Allow inbound: Port 80 (HTTP), 443 (HTTPS), 5000 (Flask)
```

#### Option 2: AWS ECS (Elastic Container Service)

```bash
# 1. Push image to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag ids-flask-app:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/ids-flask-app:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ids-flask-app:latest

# 2. Create ECS task definition
# 3. Create ECS service with load balancer
# 4. Configure auto-scaling
```

#### Option 3: AWS Elastic Beanstalk

```bash
# 1. Install EB CLI
pip install awsebcli

# 2. Initialize EB application
eb init -p docker ids-flask-app --region us-east-1

# 3. Create environment
eb create ids-production

# 4. Deploy
eb deploy

# 5. Open application
eb open
```

### Azure Deployment

#### Azure Container Instances

```bash
# 1. Login to Azure
az login

# 2. Create resource group
az group create --name ids-rg --location eastus

# 3. Create container registry
az acr create --resource-group ids-rg --name idsregistry --sku Basic

# 4. Build and push image
az acr build --registry idsregistry --image ids-flask-app:latest .

# 5. Deploy container
az container create \
  --resource-group ids-rg \
  --name ids-app \
  --image idsregistry.azurecr.io/ids-flask-app:latest \
  --dns-name-label ids-unique-name \
  --ports 5000
```

#### Azure App Service

```bash
# Deploy directly from Docker Hub or ACR
az webapp create \
  --resource-group ids-rg \
  --plan ids-plan \
  --name ids-webapp \
  --deployment-container-image-name ids-flask-app:latest
```

### Google Cloud Platform

#### Google Cloud Run

```bash
# 1. Enable Cloud Run API
gcloud services enable run.googleapis.com

# 2. Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/ids-flask-app

# 3. Deploy to Cloud Run
gcloud run deploy ids-app \
  --image gcr.io/PROJECT_ID/ids-flask-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Heroku Deployment

```bash
# 1. Login to Heroku
heroku login

# 2. Create app
heroku create ids-flask-app

# 3. Set buildpack for Python
heroku buildpacks:set heroku/python

# 4. Deploy
git push heroku main

# 5. Scale dynos
heroku ps:scale web=1

# 6. Open app
heroku open
```

Create `Procfile`:
```
web: waitress-serve --port=$PORT flask_app:app
```

---

## ✅ Production Checklist

### Security

- [ ] Change default SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS origins properly
- [ ] Implement rate limiting
- [ ] Add authentication/authorization
- [ ] Set up firewall rules
- [ ] Disable debug mode (`DEBUG=False`)
- [ ] Secure environment variables
- [ ] Implement input validation
- [ ] Set up security headers (Talisman)

### Configuration

```python
# Production config
app.config['DEBUG'] = False
app.config['TESTING'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

### Performance

- [ ] Use production WSGI server (Gunicorn/Waitress)
- [ ] Enable caching (Redis/Memcached)
- [ ] Configure CDN for static assets
- [ ] Optimize database queries
- [ ] Enable gzip compression
- [ ] Set up load balancing
- [ ] Configure auto-scaling

### Monitoring

- [ ] Set up application logging
- [ ] Configure error tracking (Sentry)
- [ ] Enable performance monitoring (New Relic/DataDog)
- [ ] Set up uptime monitoring
- [ ] Configure alerting
- [ ] Enable health checks

### Backup

- [ ] Backup trained models regularly
- [ ] Backup database (if used)
- [ ] Version control configurations
- [ ] Document recovery procedures

---

## 📊 Monitoring & Maintenance

### Application Logs

```bash
# View logs (Docker)
docker-compose logs -f ids-app

# Save logs to file
docker-compose logs ids-app > app.log

# Tail last 100 lines
docker-compose logs --tail=100 ids-app
```

### Health Checks

```bash
# Check application status
curl http://localhost:5000/api/status

# Check with authentication
curl -H "Authorization: Bearer TOKEN" http://localhost:5000/api/status
```

### Updating Application

```bash
# Pull latest changes
git pull origin main

# Rebuild Docker image
docker-compose up -d --build

# Or without downtime
docker-compose build
docker-compose up -d --no-deps ids-app
```

### Database Migrations (if applicable)

```bash
# Run migrations
docker-compose exec ids-app python manage.py migrate

# Create backup before migration
docker-compose exec ids-app python manage.py dumpdata > backup.json
```

---

## 🔧 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Find process using port 5000
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # Linux/Mac

# Kill process
taskkill /PID <PID> /F        # Windows
kill -9 <PID>                 # Linux/Mac
```

**Models not loading:**
```bash
# Ensure models are trained
docker-compose exec ids-app python src/train_model.py

# Check models directory
docker-compose exec ids-app ls -la models/
```

**Memory issues:**
```bash
# Increase Docker memory limit (Docker Desktop)
# Settings → Resources → Memory → 4GB+

# Check container memory usage
docker stats ids-app
```

**Permission errors:**
```bash
# Fix file permissions
chmod -R 755 .
chown -R $USER:$USER .
```

---

## 📚 Additional Resources

- [Flask Deployment Options](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [AWS Deployment Guide](https://docs.aws.amazon.com/)
- [Azure Documentation](https://docs.microsoft.com/azure/)
- [GCP Documentation](https://cloud.google.com/docs)

---

## 🆘 Support

For deployment issues:
1. Check application logs
2. Verify all prerequisites are met
3. Review this documentation
4. Contact the development team

---

**Last Updated**: November 21, 2026  
**Version**: 1.0.0
