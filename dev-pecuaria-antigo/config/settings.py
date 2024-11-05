import os
from datetime import timedelta
from decouple import config
from django.conf import settings
from django.contrib.messages import constants as messages
from import_export.formats.base_formats import CSV, XLSX
from pathlib import Path

# Variáveis de ambiente sensíveis -> .env
SECRET_KEY = config('SECRET_KEY')
NAME_BANCO = config('NAME_BANCO')
USER_BANCO = config('USER_BANCO')
PASSWORD_BANCO = config('PASSWORD_BANCO')
HOST_BANCO = config('HOST_BANCO')
PORT_BANCO = config('PORT_BANCO')


DEBUG = True  # Alterar para False em produção

ALLOWED_HOSTS = ['campusinteligentetest.ifsuldeminas.edu.br', '127.0.0.1', 'localhost']  

CSRF_TRUSTED_ORIGINS = ['https://*.br','http://*.br'] 

BASE_DIR = Path(__file__).resolve().parent.parent

# Configuração do banco de dados
DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.sqlite3',
        "NAME": BASE_DIR / 'db.sqlite',
    }
}

# Aplicativos instalados no projeto
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    "rest_framework",
    'rest_framework_simplejwt',
    "import_export",
    "nested_admin",
    "crispy_forms",
    "crispy_bootstrap5",

    # Aplicativos sendo trabalhados
    # "apps.agricola",
    "apps.core",
    # "apps.dispositivos",
    "apps.edificios",
    "apps.feedback",
    "apps.industria",
    # "apps.maquinas",
    "apps.pecuaria",
    "apps.seguranca",
]

# Configuração do Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Configuração do Django
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Configuração de rotas -> começa pelas urls de config
ROOT_URLCONF = "config.urls"

# Configuração de templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # Templates das demais aplicações
            os.path.join(BASE_DIR, "apps/core/templates/"),
            os.path.join(BASE_DIR, "apps/agricola/templates/"),
            os.path.join(BASE_DIR, "apps/dispositivos/templates/"),
            os.path.join(BASE_DIR, "apps/edificios/templates/"),
            os.path.join(BASE_DIR, "apps/feedback/templates/"),
            os.path.join(BASE_DIR, "apps/industria/templates/"),
            os.path.join(BASE_DIR, "apps/maquinas/templates/"),
            os.path.join(BASE_DIR, "apps/pecuaria/templates/"),
            os.path.join(BASE_DIR, "apps/seguranca/templates/"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Validação de senha
AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
]

# Padronização de URL -> adiciona barra no final quando True
APPEND_SLASH = False

# Configuração de região e fuso horário
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"

# Configuração de localização
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Configuração de formato de data e hora
DATE_INPUT_FORMATS = ["%d-%m-%Y"]  # Data no formato 'dd-mm-yy'
DATETIME_INPUT_FORMATS = [
    "%d-%m-%Y %H:%M:%S"
]  # Data e hora no formato 'dd-mm-yy hh:mm:ss'

# Configuração de arquivos estáticos
# URL para arquivos estáticos
STATIC_URL = "static/"
# Caminho absoluto para a pasta 'static'
STATIC_ROOT = os.path.join(STATIC_URL, "static")
# Locais adicionais para arquivos estáticos
STATICFILES_DIRS = [
    # Diretório 'static' das demais aplicações
    os.path.join(BASE_DIR, "apps/core/static/"),
    os.path.join(BASE_DIR, "apps/agricola/static/"),
    os.path.join(BASE_DIR, "apps/dispositivos/static/"),
    os.path.join(BASE_DIR, "apps/edificios/static/"),
    os.path.join(BASE_DIR, "apps/feedback/static/"),
    os.path.join(BASE_DIR, "apps/industria/static/"),
    os.path.join(BASE_DIR, "apps/maquinas/static/"),
    os.path.join(BASE_DIR, "apps/pecuaria/static/"),
    os.path.join(BASE_DIR, "apps/seguranca/static/"),
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configuração do Django Rest Framework
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DATETIME_FORMAT': '%d/%m/%Y %H:%M:%S',
    'DATE_FORMAT': '%d/%m/%Y',
    'DATE_INPUT_FORMATS': ['%d/%m/%Y'],
}

# Configuração do Simple JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": settings.SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

# Import Export
IMPORT_FORMATS = [
    CSV,
    XLSX,
]

EXPORT_FORMATS = [
    CSV,
    XLSX,
]

# Messages
MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}