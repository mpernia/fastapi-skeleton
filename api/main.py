import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
import structlog
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from api.config.docs import *
from api.config.cors import *
from api.config.resources import API_NAME, API_VERSION, API_DESCRIPTION, API_PREFIX
from api.config.settings import get_settings
from api.middlewares.logging import LoggingMiddleware
from api.middlewares.rate_limit import RateLimitMiddleware
from api.routes.api import router

# Load environment variables
load_dotenv()

settings = get_settings()

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()

# Initialize Sentry if DSN is provided and not empty
if settings.SENTRY_DSN and settings.SENTRY_DSN.strip():
    try:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.ENVIRONMENT,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
            integrations=[
                FastApiIntegration(
                    transaction_style="endpoint"
                ),
                RedisIntegration(),
                SqlalchemyIntegration(),
            ]
        )
        logger.info("Sentry initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Sentry: {str(e)}")
else:
    logger.info("Sentry DSN not configured, skipping Sentry initialization")

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup
    logger.info("Starting up application", environment=settings.ENVIRONMENT)
    yield
    # Shutdown
    logger.info("Shutting down application")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A modern FastAPI application with batteries included",
    openapi_tags=tags_metadata,
    terms_of_service=terms_url,
    contact=contact_info,
    license_info=license_info,
    lifespan=lifespan,
)

# Add middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY.get_secret_value())
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)

# Mount metrics endpoint for Prometheus
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Mount static files
app.mount("/public", StaticFiles(directory='public'), name='public')
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API router
app.include_router(router, prefix=settings.API_PREFIX)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        "Unhandled exception",
        exc_info=True,
        request_path=str(request.url),
        error=str(exc),
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

@app.get("/health")
async def health_check() -> dict:
    return {"status": "healthy", "version": settings.APP_VERSION}

@app.get("/docs", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url='/openapi.json',
        title=API_NAME,
        swagger_favicon_url='/public/assets/img/favicon.png'
    )


@app.get("/redoc", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(
        openapi_url='/openapi.json',
        title=API_NAME,
        redoc_favicon_url='/public/assets/img/favicon.png'
    )


@app.get('/', tags=['Root'])
def root():
    return RedirectResponse(url=API_PREFIX, status_code=303)


@app.get(API_PREFIX, include_in_schema=False, tags=['Root'])
def actual_version():
    return {'Hello': 'World'}
