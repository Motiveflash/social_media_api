**Security Documentation for Social Media API**

This document outlines the measures taken to secure the Social Media API built using Django and Django REST Framework. The security practices implemented ensure the integrity, confidentiality, and availability of the API and its data.

---

### **1. Environment Variables**
Sensitive information such as the Django secret key, database credentials, and other configuration settings are stored in a `.env` file and loaded using the `python-decouple` package.

#### Implementation Steps:
1. Install `python-decouple`:
   ```bash
   pip install python-decouple
   ```

2. Refactor `settings.py`:
   ```python
   from decouple import config

   SECRET_KEY = config('SECRET_KEY')
   DEBUG = config('DEBUG', default=False, cast=bool)
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': config('DB_NAME'),
           'USER': config('DB_USER'),
           'PASSWORD': config('DB_PASSWORD'),
           'HOST': config('DB_HOST', default='127.0.0.1'),
           'PORT': config('DB_PORT', default='5432'),
       }
   }
   ```

3. Create a `.env` file to store sensitive data:
   ```env
   SECRET_KEY=your_super_secret_key
   DEBUG=False
   DB_NAME=social_media_api
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=5432
   ```

4. Add `.env` to `.gitignore`:
   ```bash
   echo ".env" >> .gitignore
   ```

---

### **2. Authentication**
Authentication is secured using JSON Web Tokens (JWT), ensuring stateless and secure user authentication.

#### Implementation Steps:
1. Install `djangorestframework-simplejwt`:
   ```bash
   pip install djangorestframework-simplejwt
   ```

2. Configure JWT in `settings.py`:
   ```python
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': (
           'rest_framework_simplejwt.authentication.JWTAuthentication',
       ),
   }
   ```

3. Add JWT endpoints in `urls.py`:
   ```python
   from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

   urlpatterns += [
       path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
       path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   ]
   ```

4. Test JWT:
   - Use `/api/token/` to obtain an access and refresh token.
   - Use `/api/token/refresh/` to refresh expired tokens.

---

### **3. HTTPS**
The API is deployed on platforms like Heroku, which provide HTTPS by default, ensuring encrypted communication between clients and the server.

#### Best Practices:
- Redirect all HTTP traffic to HTTPS.
- Set `SECURE_SSL_REDIRECT = True` in production.

---

### **4. Permissions**
Permissions ensure that only authorized users can access or modify specific resources.

#### Implementation:
1. Configure custom permissions for views and serializers to enforce access rules.
2. Example for securing post update/delete operations:
   ```python
   from rest_framework.permissions import BasePermission

   class IsOwnerOrReadOnly(BasePermission):
       def has_object_permission(self, request, view, obj):
           if request.method in ('GET', 'HEAD', 'OPTIONS'):
               return True
           return obj.author == request.user
   ```

3. Apply the permission to a view:
   ```python
   class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
       queryset = Post.objects.all()
       serializer_class = PostSerializer
       permission_classes = [IsOwnerOrReadOnly]
   ```

---

### **5. Secure HTTP Headers**
Django’s `django-secure` middleware is used to add secure HTTP headers such as `Content-Security-Policy`, `X-Frame-Options`, and `X-Content-Type-Options`.

#### Implementation:
1. Add the `SecurityMiddleware` to `MIDDLEWARE` in `settings.py`:
   ```python
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       ...
   ]
   ```

2. Set secure headers:
   ```python
   SECURE_CONTENT_TYPE_NOSNIFF = True
   SECURE_BROWSER_XSS_FILTER = True
   X_FRAME_OPTIONS = 'DENY'
   SECURE_HSTS_SECONDS = 31536000  # 1 year
   SECURE_HSTS_INCLUDE_SUBDOMAINS = True
   SECURE_HSTS_PRELOAD = True
   ```

---

### **6. Static and Media File Handling**
Static and media files are served securely using `WhiteNoise` and cloud services (e.g., AWS S3) for production.

#### Implementation:
1. Install `whitenoise`:
   ```bash
   pip install whitenoise
   ```

2. Configure `settings.py`:
   ```python
   MIDDLEWARE = [
       'whitenoise.middleware.WhiteNoiseMiddleware',
       ...
   ]

   STATIC_URL = '/static/'
   STATIC_ROOT = BASE_DIR / 'staticfiles'
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   ```

3. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

4. Use a cloud storage service for media files, such as AWS S3.

---

### **7. Deployment Security**
The application is deployed on Heroku with the following security measures:

1. Set environment variables securely in Heroku:
   ```bash
   heroku config:set SECRET_KEY=your_super_secret_key
   heroku config:set DEBUG=False
   ```

2. Ensure database connections are encrypted.
3. Regularly update packages and dependencies.

---

### **8. Monitoring and Error Logging**
Use tools like Sentry for monitoring errors and logging suspicious activity.

#### Implementation:
1. Install Sentry:
   ```bash
   pip install sentry-sdk
   ```

2. Integrate with Django:
   ```python
   import sentry_sdk
   from sentry_sdk.integrations.django import DjangoIntegration

   sentry_sdk.init(
       dsn="your_sentry_dsn",
       integrations=[DjangoIntegration()],
   )
   ```

---

These security measures ensure a robust and secure Social Media API while adhering to best practices for API development and deployment.

