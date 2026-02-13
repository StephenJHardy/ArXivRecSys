# Deployment Guide

This guide covers the deployment of the ArXiv Recommendation System in different environments.

## Development Environment

### Prerequisites
- Docker and Docker Compose
- Node.js v16+
- Python 3.8+
- Git

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ArXivRecSys.git
cd ArXivRecSys
```

2. Set up environment variables:
```bash
cp client/.env.example client/.env
cp backend/.env.example backend/.env
```

3. Start the development environment:
```bash
docker-compose up
```

## Production Environment

### Option 1: Docker Compose Deployment

1. Clone the repository on your production server:
```bash
git clone https://github.com/yourusername/ArXivRecSys.git
cd ArXivRecSys
```

2. Create production environment files:
```bash
cp client/.env.example client/.env.production
cp backend/.env.example backend/.env.production
```

3. Edit the environment files with production values:
```bash
# backend/.env.production
DATABASE_URL=postgresql://user:password@db:5432/arxiv_recsys
SECRET_KEY=your-secure-secret-key
```

4. Build and start the production containers:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Option 2: Kubernetes Deployment

1. Install required tools:
- kubectl
- helm

2. Create Kubernetes secrets:
```bash
kubectl create secret generic arxiv-recsys-secrets \
  --from-literal=DB_PASSWORD=your-db-password \
  --from-literal=SECRET_KEY=your-secret-key
```

3. Deploy using Helm:
```bash
helm install arxiv-recsys ./helm
```

### Option 3: Cloud Platform Deployment

#### AWS Deployment

1. Set up AWS infrastructure:
- EC2 instances or ECS cluster
- RDS PostgreSQL database
- Elastic Load Balancer
- Route 53 for DNS

2. Configure AWS CLI:
```bash
aws configure
```

3. Deploy using AWS CLI:
```bash
aws ecs create-cluster --cluster-name arxiv-recsys
aws ecs register-task-definition --cli-input-json file://task-definition.json
aws ecs create-service --cli-input-json file://service-definition.json
```

#### Google Cloud Platform

1. Set up GCP infrastructure:
- GKE cluster
- Cloud SQL PostgreSQL
- Load Balancer
- Cloud DNS

2. Configure gcloud:
```bash
gcloud auth login
gcloud config set project your-project-id
```

3. Deploy to GKE:
```bash
gcloud container clusters get-credentials your-cluster
kubectl apply -f k8s/
```

## SSL/TLS Configuration

### Using Let's Encrypt

1. Install certbot:
```bash
apt-get update
apt-get install certbot python3-certbot-nginx
```

2. Obtain certificate:
```bash
certbot --nginx -d yourdomain.com
```

### Manual SSL Configuration

1. Configure Nginx with SSL:
```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Other SSL settings...
}
```

## Monitoring and Maintenance

### Setting up Monitoring

1. Install Prometheus and Grafana:
```bash
helm install prometheus prometheus-community/prometheus
helm install grafana grafana/grafana
```

2. Configure monitoring dashboards in Grafana:
- System metrics
- Application metrics
- Database metrics

### Backup Strategy

1. Database backups:
```bash
# Daily backup script
pg_dump -U postgres arxiv_recsys > backup_$(date +%Y%m%d).sql
```

2. Application data backups:
```bash
# Backup script for user data
tar -czf user_data_$(date +%Y%m%d).tar.gz /path/to/data
```

### Scaling

1. Horizontal scaling:
```bash
# Kubernetes
kubectl scale deployment arxiv-recsys --replicas=3

# Docker Compose
docker-compose up --scale backend=3
```

2. Vertical scaling:
- Increase instance resources
- Upgrade database tier

## Troubleshooting

### Common Issues

1. Database connection issues:
```bash
# Check database connectivity
pg_isready -h db -U postgres
```

2. Application logs:
```bash
# View backend logs
docker-compose logs backend

# View frontend logs
docker-compose logs client
```

3. Performance issues:
```bash
# Monitor system resources
htop
docker stats
```

## Security Considerations

1. Enable security features:
- Rate limiting
- WAF rules
- DDoS protection

2. Regular updates:
```bash
# Update dependencies
pip install --upgrade -r requirements.txt
npm update

# Update system packages
apt-get update && apt-get upgrade
```

3. Security scanning:
```bash
# Run security scans
docker scan arxiv-recsys-backend
npm audit
``` 