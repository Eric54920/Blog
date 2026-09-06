import json
import os
from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name, default=None):
    value = os.getenv(name)
    if value is None:
        return default or []
    return [item.strip() for item in value.split(",") if item.strip()]


def env_json(name, default=None):
    value = os.getenv(name)
    if not value:
        return default if default is not None else {}
    return json.loads(value)


# Keep the historical default only for backward compatibility. Set a unique
# DJANGO_SECRET_KEY before deploying or before running in Docker.
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", '+%@zdh)6xuv^)&&@781zx9))9+pwo1lw%c@@in^yd2kl$t&rn*')

DEBUG = env_bool("DJANGO_DEBUG", True)

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", ["*"])

CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "web.apps.WebConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "web.middlewares.auth.AuthMiddleWare",
]

ROOT_URLCONF = "Blog.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR / "web" / "templates")],
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

WSGI_APPLICATION = "Blog.wsgi.application"


# Database
# Local development defaults to SQLite. Docker Compose overrides these with
# MySQL connection values.
db_engine = os.getenv("DB_ENGINE", "django.db.backends.sqlite3")
db_name = os.getenv("DB_NAME", "db.sqlite3")

DATABASES = {
    "default": {
        "ENGINE": db_engine,
        "NAME": db_name,
    }
}

if db_engine.endswith("sqlite3"):
    sqlite_path = Path(db_name).expanduser()
    DATABASES["default"]["NAME"] = sqlite_path if sqlite_path.is_absolute() else BASE_DIR / sqlite_path
else:
    DATABASES["default"].update(
        {
            "HOST": os.getenv("DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DB_PORT", "3306"),
            "USER": os.getenv("DB_USER", "blog"),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
        }
    )
    db_options = os.getenv("DB_OPTIONS")
    if db_options:
        DATABASES["default"]["OPTIONS"] = json.loads(db_options)


# Password validation
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


# Internationalization
LANGUAGE_CODE = "zh-Hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# App assets live in web/static and are found automatically by Django.
STATIC_URL = "/static/"

STATIC_ROOT = str(BASE_DIR / "staticfiles")

STORAGES = {
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if DEBUG
            else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        )
    }
}


# Site profile used by web/templatetags/global.py and album.py
LOGO = os.getenv("SITE_LOGO", "images/avatar.png")
AVATAR = os.getenv("SITE_AVATAR", "images/avatar.png")
SITE_NAME = os.getenv("SITE_NAME", "我的小站")
AUTHOR = os.getenv("SITE_AUTHOR", "Eric")
SIGNATURE = os.getenv("SITE_SIGNATURE", "千里之行，始于足下")
KEYWORDS = os.getenv("SITE_KEYWORDS", "Python,Django,Blog")
DESC = os.getenv("SITE_DESCRIPTION", "这是一个基于 Django 的博客系统")
ALBUM_DESC = os.getenv("ALBUM_DESCRIPTION", "分享点滴，记录美好")
ALBUM_HEADIMG = os.getenv("ALBUM_HEADIMG", "")
COPY_RIGHT = os.getenv("SITE_COPYRIGHT", "Copyright © 2024 Eric")
SOCIAL = env_json("SITE_SOCIAL")
SITE_VERIFICATION = env_json("SITE_VERIFICATION")

COLOR_LIST = {
    "Python": "#3572A5",
    "HTML": "#e34c26",
    "JavaScript": "#f1e05a",
    "CSS": "#563d7c",
    "PHP": "#4F5D95",
    "Vue": "#2c3e50",
    "C++": "#f34b7d",
    "C#": "#178600",
    "Kotlin": "#F18E33",
    "Java": "#b07219",
    "Go": "#00ADD8",
    "Swift": "#ffac45",
    "Shell": "#89e051",
    "Lua": "#000080",
    "C": "#555555",
    "Perl": "#0298c3",
    "Scala": "#c22d40",
    "Objective-C": "#438eff",
    "Ruby": "#701516",
    "Linux": "#f6bf03",
    "爬虫": "#b02f2f",
    "网络": "#60a9f5",
    "算法": "#902ea1",
    "TypeScript": "#2b7489",
    "MySQL": "#d28a36",
    "机器学习": "#7ac32b",
    "Redis": "#d70b0b",
    "数据分析": "#08a371",
    "Django": "#0C4B33",
    "Docker": "#0073EC",
    "Git": "#d83812",
}


# Public paths that do not require an administrator login.
WHITE_REGEX_URL_LIST = [
    "/$",
    "/login",
    "/article/\\d+",
    "/archives",
    "/album",
    "/album/\\d+",
    "/about",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
