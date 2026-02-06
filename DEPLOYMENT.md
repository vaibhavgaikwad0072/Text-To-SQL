# Deployment Guide - Text-to-SQL Pipeline

## Overview
This guide covers deploying the Text-to-SQL pipeline to various environments.

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Platforms](#cloud-platforms)
4. [Production Checklist](#production-checklist)

---

## Local Development

### Quick Start
```bash
# Windows
run.bat

# Mac/Linux
make setup
make run-interactive
```

### Development Mode
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup environment
python setup.py

# 3. Run tests
python test_pipeline.py

# 4. Start development server
streamlit run app.py
```

### With Database
```bash
# Start MySQL (Docker)
docker run --name mysql \
  -e MYSQL_ROOT_PASSWORD=vaibhav \
  -e MYSQL_DATABASE=regional_sales_data \
  -p 3306:3306 \
  -d mysql:8.0

# Then run the app
streamlit run app.py
```

---

## Docker Deployment

### Single Container (App Only)
```bash
# Build image
docker build -t text-to-sql:latest .

# Run container
docker run -p 8501:8501 \
  -e DB_HOST=localhost \
  -e DB_USER=root \
  -e DB_PASSWORD=vaibhav \
  -e GOOGLE_API_KEY=your_key \
  text-to-sql:latest
```

### Docker Compose (Full Stack)
```bash
# Create .env file with credentials
cat > .env << EOF
DB_HOST=mysql
DB_USER=root
DB_PASSWORD=vaibhav
DB_NAME=regional_sales_data
GOOGLE_API_KEY=your_api_key
EOF

# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### Docker Compose with Data Import
```bash
# Add to docker-compose.yml mysql service:
init:
  - echo "LOAD DATA LOCAL INFILE 'Data_CSV/Customers.csv' INTO TABLE customers FIELDS TERMINATED BY ',' IGNORE 1 ROWS;" | mysql -h mysql -u root -pvaibhav regional_sales_data
```

---

## Cloud Platforms

### Heroku

#### Setup
```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create text-to-sql

# Set up MySQL add-on
heroku addons:create cleardb:ignite
```

#### Configuration
```bash
# Set environment variables
heroku config:set GOOGLE_API_KEY=your_key
heroku config:set DB_HOST=your_db_host

# View config
heroku config
```

#### Deploy
```bash
# Create Procfile
echo "web: streamlit run app.py --server.port 8500" > Procfile

# Deploy
git push heroku main

# Check logs
heroku logs --tail
```

### AWS EC2

#### Setup
```bash
# 1. Launch EC2 instance (Ubuntu 20.04)
# 2. SSH into instance
ssh -i key.pem ubuntu@your-instance.amazonaws.com

# 3. Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv
sudo apt install mysql-server mysql-client

# 4. Clone repository
git clone your-repo
cd Text-To-SQL

# 5. Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Configure .env
nano .env
```

#### Running as Service
```bash
# Create systemd service
sudo tee /etc/systemd/system/text-to-sql.service > /dev/null << EOF
[Unit]
Description=Text-to-SQL Pipeline
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/Text-To-SQL
ExecStart=/home/ubuntu/Text-To-SQL/venv/bin/streamlit run app.py --server.port 8501
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl enable text-to-sql
sudo systemctl start text-to-sql
sudo systemctl status text-to-sql
```

#### With Nginx Reverse Proxy
```bash
# Install Nginx
sudo apt install nginx

# Create config
sudo tee /etc/nginx/sites-available/text-to-sql > /dev/null << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/text-to-sql /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Google Cloud Run

#### Setup
```bash
# Install Cloud SDK
curl https://sdk.cloud.google.com | bash

# Login
gcloud auth login

# Create project
gcloud projects create text-to-sql-app
gcloud config set project text-to-sql-app
```

#### Deploy with Docker
```bash
# Build image
gcloud builds submit --tag gcr.io/text-to-sql-app/text-to-sql

# Deploy
gcloud run deploy text-to-sql \
  --image gcr.io/text-to-sql-app/text-to-sql \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=your_key,DB_HOST=your_host
```

---

## Production Checklist

### Security
- [ ] Use environment variables for all secrets
- [ ] Never commit .env files
- [ ] Use strong database passwords
- [ ] Enable database authentication
- [ ] Use HTTPS/SSL certificates
- [ ] Enable firewall rules
- [ ] Restrict database access by IP
- [ ] Implement API rate limiting
- [ ] Add authentication to web interface
- [ ] Encrypt sensitive data

### Performance
- [ ] Set up database indexes
- [ ] Configure connection pooling
- [ ] Enable caching layer (Redis)
- [ ] Use CDN for static files
- [ ] Optimize database queries
- [ ] Monitor query performance
- [ ] Set up load balancer
- [ ] Use auto-scaling

### Monitoring & Logging
- [ ] Set up centralized logging
- [ ] Configure alerting
- [ ] Monitor system resources
- [ ] Track API usage
- [ ] Set up error tracking
- [ ] Enable audit logging
- [ ] Monitor database performance
- [ ] Track LLM usage/costs

### Backup & Recovery
- [ ] Automated database backups
- [ ] Test restore procedures
- [ ] Backup configuration files
- [ ] Document disaster recovery
- [ ] Version control code
- [ ] Backup application logs

### Deployment Best Practices
- [ ] Use CI/CD pipeline
- [ ] Automated testing before deploy
- [ ] Blue-green deployment strategy
- [ ] Rollback procedures documented
- [ ] Health checks configured
- [ ] Gradual traffic shifting

### Documentation
- [ ] API documentation
- [ ] Deployment procedures
- [ ] Troubleshooting guide
- [ ] Architecture diagrams
- [ ] Change log maintained
- [ ] Emergency contacts

---

## Scaling Considerations

### Horizontal Scaling
```bash
# Use load balancer to distribute traffic
# Multiple app instances behind load balancer
# Shared database backend
```

### Vertical Scaling
```bash
# Increase instance size
# Upgrade database resources
# Increase memory/CPU allocation
```

### Database Optimization
```bash
# Connection pooling (PgBouncer, ProxySQL)
# Read replicas for scaling reads
# Sharding for large datasets
# Caching layer (Redis, Memcached)
```

### Monitoring Tools
- Prometheus for metrics
- ELK Stack for logging
- Grafana for dashboards
- New Relic/DataDog for APM
- CloudWatch (AWS) or similar

---

## Rollback Procedure

If deployment fails:
```bash
# Docker
docker-compose down
docker-compose pull
docker-compose up -d

# Heroku
heroku rollback

# AWS
# Use auto scaling groups to revert to previous version
# Or re-deploy from Git
```

---

## Monitoring & Alerts

### Key Metrics to Monitor
- Response time
- Error rate
- API call volume
- Database query time
- Uptime
- LLM token usage cost

### Alert Thresholds
- Response time > 5 seconds
- Error rate > 1%
- Database connection failures
- Out of memory conditions
- High API costs

Example Alerts:
```yaml
alert: HighErrorRate
expr: error_rate > 0.01
for: 5m
annotations:
  summary: "High error rate detected"
```

---

## Cost Optimization

### API Usage
- Monitor Gemini API calls
- Implement query caching
- Optimize prompts
- Use cheaper models when appropriate

### Infrastructure
- Right-size instances
- Use spot instances (Cloud Run, EC2)
- Enable auto-scaling
- Clean up unused resources

### Database
- Monitor query efficiency
- Archive old data
- Implement partitioning
- Use read replicas wisely

---

## Troubleshooting Deployment

### Application Won't Start
```bash
# Check logs
docker-compose logs app

# Verify environment
echo $GOOGLE_API_KEY
echo $DB_HOST

# Test connectivity
curl http://localhost:8501
```

### Database Connection Issues
```bash
# Test connection
mysql -h $DB_HOST -u $DB_USER -p

# Check network rules
# Verify security groups
# Check firewall
```

### Performance Issues
```bash
# Monitor system resources
htop
docker stats

# Check database performance
SHOW PROCESSLIST;
SHOW SLOW LOGS;

# Profile code
python -m cProfile -o output.prof app.py
```

---

## Additional Resources

- [Streamlit Deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Kubernetes Basics](https://kubernetes.io/docs/basics/)
- [AWS Best Practices](https://aws.amazon.com/architecture/best-practices/)

---

For support or questions, refer to README.md
