"""
Django settings for travel_buddy project.

Generated by 'django-admin startproject' using Django 4.2.18.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
#we want to import our env here, defensive programming tho, only import if it exists
import os
import dj_database_url
if os.path.isfile('env.py'):
    import env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# Paths for our static, templates and other directories
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ANON_MODE = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '111.222.333.444',
    'mywebsite.example',
    '.herokuapp.com',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'django_extensions',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_summernote',
    'recommendations',
    'profiles.apps.ProfilesConfig',
    'core',
]

# Our login urls and site id, we need a site id for every project in our app
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# we add heroku and the code institute ide as csrf trusted 
# for running our db ect
CSRF_TRUSTED_ORIGINS = [
	"https://*.codeinstitute-ide.net/", 
    "https://*.herokuapp.com" ,
]

ROOT_URLCONF = 'travel_buddy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'travel_buddy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# we're also going to import our own db url for the code institute db
DATABASES = {
    'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

### EMAIL SETUP

# Require an email
ACCOUNT_EMAIL_REQUIRED = True
# Require a username
ACCOUNT_USERNAME_REQUIRED = True
# Options: "none", "optional", "mandatory"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# Allows login with username or email
ACCOUNT_AUTHENTICATION_METHOD = "username_email"  

### --- Email settings --- ###

#backend - our email backend that django will use to connect
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#the email host backend
EMAIL_HOST = 'smtp.gmail.com' 
#port we will send it on and if we will use tls
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#the email account django will send from
EMAIL_HOST_USER = os.environ.get("HOST_EMAIL")
EMAIL_HOST_PASSWORD = os.environ.get("HOST_PW")

#the default / forward facing email users will see
DEFAULT_FROM_EMAIL = "Travel Buddy Team <noreply@travelbuddy.com>"

#the verification requirement (we want mandatory to ensure verified users)
ACCOUNT_EMAIL_VERIFICATION = 'optional' 

#the redirect for when the user authenticates
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = 'recommended'

#also we will use these additional defualts
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[Travel Buddy] "

### --- Internationalization --- ###

# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

### --- Static files (CSS, JavaScript, Images) --- ### 

# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

### --- Default primary key field type --- ### 
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

### --- Default login/logout redirect urls --- ### 

# these don't seem like a lot but we want the user to stay on recommendations
# page when they log in or out.
LOGOUT_REDIRECT_URL = 'recommendations'
LOGIN_REDIRECT_URL = 'recommendations'