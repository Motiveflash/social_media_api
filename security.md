# Security Configuration for Social Media API

This document provides an overview of the security features implemented in the `social_media_api` project. These settings ensure that the application adheres to best practices for security in Django applications.

---

## Secret Management

- **`SECRET_KEY`**: The secret key is stored in environment variables and accessed using `python-decouple`. This ensures it is not exposed in the codebase.

```python
SECRET_KEY = config('SECRET_KEY')
```

## Debug Mode

- Debug mode is controlled by an environment variable. By default, `DEBUG` is set to `False` in production to avoid leaking sensitive information in error pages.

```python
DEBUG = config('DEBUG', default=False, cast=bool)
```

## Allowed Hosts

- The `ALLOWED_HOSTS` setting ensures the application only responds to requests from specific domains or IPs, which are specified via environment variables.

```python
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')
```

## Middleware for Security

### Security Middleware
- **`django.middleware.security.SecurityMiddleware`**: Provides basic security enhancements such as HTTPS redirection and XSS protection.
- **`whitenoise.middleware.WhiteNoiseMiddleware`**: Serves static files securely.

### CORS Middleware
- Enables Cross-Origin Resource Sharing (CORS) for trusted origins.

```python
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='').split(',')
```

## HTTPS and Cookie Security

- Enforced use of HTTPS for all requests:
  - **`SECURE_SSL_REDIRECT`**: Redirects all HTTP traffic to HTTPS.
  - **`SECURE_HSTS_SECONDS`**: Enables HTTP Strict Transport Security (HSTS) for one year.
  - **`SECURE_HSTS_INCLUDE_SUBDOMAINS`**: Extends HSTS to subdomains.
  - **`SECURE_HSTS_PRELOAD`**: Indicates readiness for HSTS preloading.
- Cookies are secured to prevent transmission over unsecured channels:
  - **`SESSION_COOKIE_SECURE`**: Ensures session cookies are only sent over HTTPS.
  - **`CSRF_COOKIE_SECURE`**: Secures the CSRF cookie.
- Additional protections:
  - **`SECURE_BROWSER_XSS_FILTER`**: Activates the XSS filter in browsers.
  - **`SECURE_CONTENT_TYPE_NOSNIFF`**: Prevents the browser from interpreting files as a different MIME type.
  - **`X_FRAME_OPTIONS`**: Denies embedding the site in an iframe.

```python
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = 'DENY'
```

## Authentication and Authorization

- Uses Django REST Framework (DRF) with JWT for authentication:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

## Password Validation

- Enforces strong password policies with validators:

```python
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

## Error Logging

- Logs errors to a file for debugging purposes in development and production:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

## Deployment Considerations

- Uses **`django-heroku`** for automatic configuration in deployment environments.

```python
import django_heroku
django_heroku.settings(locals())
```

---

By following these security practices, the `social_media_api` project ensures a robust and secure environment for users and data.

