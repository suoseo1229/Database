from pathlib import Path
#디렉토리 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent 
#Django 보안 키
SECRET_KEY = 'your-secret-key'
#디버그 모드 
DEBUG = True
#허용 호스트. 배포 시 도메인 추가용
ALLOWED_HOSTS = []
#사용중인 앱 등록
INSTALLED_APPS = [
    'django.contrib.admin', #관리자페이지
    'django.contrib.auth', #인증 시스템
    'django.contrib.contenttypes', #모델 타입 정보
    'django.contrib.sessions', #세션 프레임워크
    'django.contrib.messages', #메시지 프레임워크 
    'django.contrib.staticfiles', #정적파일 관리
    'listings', #상품 관련 앱
    'accounts.apps.AccountsConfig' #signals.py 작동 
]
MIDDLEWARE = [ #요청 처리 중간단계 설정
    'django.middleware.security.SecurityMiddleware', #보안 관련 설정
    'django.contrib.sessions.middleware.SessionMiddleware', #세션 관리
    'django.middleware.common.CommonMiddleware', #공통 기능 
    'django.middleware.csrf.CsrfViewMiddleware', #CSRF 보호
    'django.contrib.auth.middleware.AuthenticationMiddleware', #로그인,인증 관리
    'django.contrib.messages.middleware.MessageMiddleware', #메시지관리
]
ROOT_URLCONF = 'Database.urls'
TEMPLATES = [ #템플릿 렌더링 
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], #사용자 정의 템플릿 경로 추가 가능하게
        'APP_DIRS': True, #앱 내 templates 폴더 자동 인식
        'OPTIONS': {
            'context_processors': [ #템플릿에서 context 사용
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
#WSGI 애플리케이션 설정 (배포 시 사용)
WSGI_APPLICATION = 'Database.wsgi.application'
#SQLite3 사용
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True #다국어 지원
USE_L10N = True #현지화 지원
USE_TZ = True #타임존 사용

STATIC_URL = '/static/' #정적 파일 경로

LOGIN_REDIRECT_URL = '/' #로그인 시 메인으로 이동
LOGOUT_REDIRECT_URL = '/login'#로그아웃 시 로그인 화면으로 이동
#자동 필드 기본값 설정
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/' #미디어파일 URL 접근 경로
MEDIA_ROOT = BASE_DIR / 'media'#미디어 저장 경로
