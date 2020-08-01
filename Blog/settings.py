import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+%@zdh)6xuv^)&&@781zx9))9+pwo1lw%c@@in^yd2kl$t&rn*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web.apps.WebConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'web.middlewares.auth.AuthMiddleWare',
]

ROOT_URLCONF = 'Blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'web/templates')],
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

WSGI_APPLICATION = 'Blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

COLOR_LIST = {'Python': '#3572A5', 'HTML': '#e34c26', 'JavaScript': '#f1e05a', 'CSS': '#563d7c', 'PHP':'#4F5D95',
              'Vue': '#2c3e50', 'C++': '#f34b7d', 'C#': '#178600', 'Kotlin': '#F18E33', 'Java': '#b07219',
              'Go': '#00ADD8', 'Swift': '#ffac45', 'Shell': '#89e051', 'Lua': '#000080', 'C': '#555555',
              'Perl': '#0298c3', 'Scala': '#c22d40', 'Objective-C': '#438eff', 'Ruby': '#701516', 'Linux': '#f6bf03',
              '爬虫': '#b02f2f', '网络': '#60a9f5', '算法': '#902ea1', 'TypeScript': '#2b7489', 'MySQL': '#d28a36',
              '机器学习': '#7ac32b', 'Redis': '#d70b0b', '数据分析': '#08a371', 'Django': '#0C4B33', 'Docker': '#0073EC', 'Git': '#d83812'}


# 白名单
WHITE_REGEX_URL_LIST = [
    "/$",
    "/login/",
    "/article/\d+",
    "/archives/",
    "/album/",
    "/album/\d+",
    "/about/"
]

try:
    from .local_settings import *
except ImportError:
    pass
