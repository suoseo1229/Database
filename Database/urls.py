from django.contrib import admin
from django.urls import path, include

import listings.urls
import accounts.urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(listings.urls)),  # 모듈 직접 참조
    path("accounts/", include(accounts.urls)),  # 모듈 직접 참조
]