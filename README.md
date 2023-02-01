# Junkyard - headless Python Django CMS
- Multi lingual
- Multi tenant
- API first


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
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'groups': 'Access to your groups'
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
