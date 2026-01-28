"""
Django settings for config project.
ARQUIVO: settings.py
OBJETIVO: Configurações globais do projeto (Banco, Apps, Pastas de Arquivos).
"""

from pathlib import Path
import os

# Caminho base do projeto (Raiz da pasta shadowrun_beyond)
BASE_DIR = Path(__file__).resolve().parent.parent

# [SEGURANÇA] Chave secreta. Não compartilhar publicamente se for subir pra produção real.
SECRET_KEY = 'django-insecure-troque-isso-se-for-pra-producao'

# [ATENÇÃO FRONTEND]
# DEBUG = True: Mostra erros detalhados na tela (Ótimo para desenvolver).
# DEBUG = False: Mostra "Erro 500/404" genérico (Modo apresentação/produção).
DEBUG = True

# [CONEXÃO]
# '*' permite que outros computadores/celulares na rede Wi-Fi acessem o site.
# Necessário para testar responsividade em dispositivos móveis.
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # [NOSSO APP]
    # Aqui é onde registramos o sistema da ficha.
    # Se criar novos apps, adicione aqui.
    'runner_sheet',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Middleware para servir arquivos estáticos de forma eficiente (opcional, mas bom ter)
    # 'whitenoise.middleware.WhiteNoiseMiddleware', 
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # [FRONTEND]
            # Forçamos o Django a olhar dentro da pasta templates do app.
            # Local dos HTMLs: runner_sheet/templates/runner_sheet/
            BASE_DIR / 'runner_sheet' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# Por padrão usamos SQLite (um arquivo simples). 
# Não precisa instalar nada extra.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# --- [CONFIGURAÇÃO DE ARQUIVOS ESTÁTICOS & MEDIA] ---
# É AQUI QUE A EQUIPE DE DESIGN DEVE PRESTAR ATENÇÃO

# URL base para acessar CSS/JS no navegador (ex: /static/style.css)
STATIC_URL = 'static/'

# [FRONTEND]
# Onde o Django procura os arquivos CSS e JS.
# Caminho físico: runner_sheet/static/
STATICFILES_DIRS = [
    BASE_DIR / "runner_sheet" / "static",
]

# Configuração para UPLOAD de imagens (Avatares dos Personagens)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'