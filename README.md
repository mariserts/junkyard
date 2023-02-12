# Junkyard - headless Python Django CMS

Developing CMS for used car parts site

- Multi project
- Multi lingual
- Multi tenant
- API first

## Endpoints

### Docs
- Swagger: http://localhost:8000/swagger/
- Redoc: http://localhost:8000/redoc/

### Authentication
- /api/authenticate/get-password-reset-link/
- /api/authenticate/authenticate/register/
- /api/authenticate/set-password/
- /api/authenticate/set-password-with-token/
- /api/authenticate/sign-in/
- /api/authenticate/sign-out/

### Cryptography
- /api/cryptography/sign/
- /api/cryptography/unsign/

### Item types
- /api/item-types/

### Languages
- /api/languages/

### Projects
- /api/projects/<project_pk>/item-types/
- /api/projects/<project_pk>/items/
- /api/projects/<project_pk>/items/<pk>/
- /api/projects/<project_pk>/items/<item_pk>/relations/ - TODO
- /api/projects/<project_pk>/items/<item_pk>/relations/<pk>/ - TODO
- /api/projects/<project_pk>/languages/
- /api/projects/<project_pk>/tenants/
- /api/projects/<project_pk>/tenants/<pk>/
- /api/projects/<project_pk>/users/
- /api/projects/<project_pk>/users/<pk>/
- /api/projects/<pk>/
- /api/projects/

### Users
- /api/users/
- /api/users/<pk>/


## Setup

### Add to settings.py

```
INSTALLED_APPS = [
    ...
    'oauth2_provider',
    'corsheaders',
    'rest_framework',
    'django_filters',
    'drf_yasg',
    'junkyard_api',
    'junkyard_api_flat_page',
    'junkyard_api_news',
]


MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
]


AUTH_USER_MODEL = 'junkyard_api.User'


AUTHENTICATION_BACKENDS = [
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
]


CORS_ORIGIN_ALLOW_ALL = True


OAUTH2_PROVIDER_APPLICATION_MODEL='junkyard_api.Application'


OAUTH2_PROVIDER = {
    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore',
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}
```


### Add to urls.py


```
urlpatterns = [
    ...
    path('', include('junkyard_api.urls')),
]
```
