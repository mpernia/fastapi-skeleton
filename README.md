# FastAPI Skeleton

A modern, production-ready FastAPI application skeleton with batteries included.

## Features

- 🚀 FastAPI framework for high performance
- 🔒 Security middleware and JWT authentication
- 📊 Prometheus metrics and Grafana dashboards
- 🔍 Structured logging with structlog
- 🐳 Docker and docker-compose setup
- 🗄️ PostgreSQL database with SQLAlchemy and Alembic migrations
- 📝 OpenAPI documentation
- 🔄 CI/CD with GitHub Actions
- 🧪 Testing setup with pytest
- 🎯 Code quality tools (black, flake8, isort, mypy)
- 🔍 Sentry integration for error tracking
- 🚦 Rate limiting middleware
- 💾 Redis caching support

## Prerequisites

- Python 3.9+
- Docker and docker-compose (optional)
- PostgreSQL (if not using Docker)
- Redis (if not using Docker)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fastapi-skeleton.git
cd fastapi-skeleton
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the example environment file:
```bash
cp .env.example .env
```

5. Update the .env file with your configuration.

## Configuration

### Port Configuration

The project uses environment variables for port configuration to avoid conflicts with other services. You can customize the ports in your `.env` file:

```bash
API_PORT=8000          # FastAPI application
POSTGRES_PORT=5432     # PostgreSQL database
REDIS_PORT=6379        # Redis cache
PROMETHEUS_PORT=9090   # Prometheus metrics
GRAFANA_PORT=3000      # Grafana dashboards
```

To change any port, simply update the corresponding variable in your `.env` file before starting the services.

## Development

1. Start the development server:
```bash
uvicorn main:app --reload
```

2. Run tests:
```bash
pytest
```

3. Run linters:
```bash
black .
flake8 .
isort .
mypy .
```

## Docker Deployment

1. Build and start the containers:
```bash
docker-compose up -d --build
```

2. Create database migrations:
```bash
docker-compose exec api alembic revision --autogenerate -m "Initial migration"
docker-compose exec api alembic upgrade head
```

## Monitoring

- Prometheus metrics: http://localhost:9090
- Grafana dashboards: http://localhost:3000

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
.
├── api/
│   ├── config/         # Configuration files
│   ├── middlewares/    # Custom middleware
│   ├── models/         # SQLAlchemy models
│   ├── routes/         # API routes
│   ├── schemas/        # Pydantic schemas
│   └── services/       # Business logic
├── migrations/         # Alembic migrations
├── tests/             # Test files
├── scripts/           # Utility scripts
├── .env.example       # Example environment variables
├── .pre-commit-config.yaml
├── alembic.ini        # Alembic configuration
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml     # Project configuration
└── requirements.txt
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
