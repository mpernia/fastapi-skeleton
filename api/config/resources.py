from api.config.settings import get_settings

settings = get_settings()

API_NAME = settings.APP_NAME
API_VERSION = settings.APP_VERSION
API_DESCRIPTION = "A modern FastAPI application with batteries included"
API_PREFIX = settings.API_PREFIX

# Security settings
AUTH_SECRET = str(settings.SECRET_KEY.get_secret_value())
AUTH_ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Session settings
SESSION_LIFETIME = settings.ACCESS_TOKEN_EXPIRE_MINUTES
SESSION_MAX_LIFETIME = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 24  # 24 hours
