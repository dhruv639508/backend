# Backend Deployment Guide

This repository contains the backend code for our application with deployment instructions and sample API implementation.

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)
- Git

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/dhruv639508/backend.git
cd backend
```

### 2. Set up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
nano .env
```

### 5. Run the Application
```bash
# Development mode
python test.py

# Production mode (if using gunicorn)
gunicorn --bind 0.0.0.0:8000 test:app
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=sqlite:///./database.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Security
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 📁 Project Structure

```
backend/
├── README.md
├── test.py                 # Sample API implementation
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── .gitignore            # Git ignore rules
├── models/               # Database models
├── routes/               # API route handlers
├── middleware/           # Custom middleware
├── tests/                # Unit tests
└── deployment/           # Deployment scripts
    ├── docker/
    ├── nginx/
    └── systemd/
```

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t backend-api .
```

### Run Container
```bash
docker run -d \
  --name backend-container \
  -p 8000:8000 \
  --env-file .env \
  backend-api
```

### Docker Compose
```bash
docker-compose up -d
```

## 🌐 Production Deployment

### Using Systemd (Linux)
```bash
# Copy service file
sudo cp deployment/systemd/backend.service /etc/systemd/system/

# Enable and start service
sudo systemctl enable backend
sudo systemctl start backend
```

### Using Nginx (Reverse Proxy)
```bash
# Copy nginx configuration
sudo cp deployment/nginx/backend.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/backend.conf /etc/nginx/sites-enabled/

# Test and reload nginx
sudo nginx -t
sudo systemctl reload nginx
```

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=./ tests/

# API endpoint testing
curl http://localhost:8000/health
```

## 📊 Monitoring

- **Health Check**: `GET /health`
- **Metrics**: `GET /metrics`
- **API Docs**: `GET /docs` (if using FastAPI)

## 🔒 Security

- Always use HTTPS in production
- Keep dependencies updated
- Use environment variables for sensitive data
- Implement proper authentication and authorization
- Enable CORS only for trusted domains

## 📝 API Documentation

The API includes the following endpoints:

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /api/users` - Get all users
- `POST /api/users` - Create a new user
- `GET /api/users/{id}` - Get user by ID

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in this repository
- Contact the development team
- Check the documentation wiki

---
**Happy Coding! 🚀**