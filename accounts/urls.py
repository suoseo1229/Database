# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views

app_name = "accounts"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html"
        ),
        name="login",
    ),

    # ✅ 커스텀 로그아웃 뷰 사용
    path("logout/", views.logout_view, name="logout"),

    path("signup/", views.signup, name="signup"),

    path("my/", views.my_page, name="my_page"),
]