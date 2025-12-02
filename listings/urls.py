# listings/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "listings"

urlpatterns = [
    # 메인 목록
    path("", views.listing_list, name="listing_list"),

    # 판매글 CRUD
    path("listing/new/", views.listing_create, name="listing_create"),
    path("listing/<int:pk>/", views.listing_detail, name="listing_detail"),
    path("listing/<int:pk>/edit/", views.listing_update, name="listing_update"),
    path("listing/<int:pk>/delete/", views.listing_delete, name="listing_delete"),

    # 찜 토글 + 찜 목록
    path("listing/<int:pk>/favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("favorites/", views.favorite_list, name="favorite_list"),

    # 내 상점
    path("my-store/<int:pk>/", views.my_store, name="my_store"),

    # 신고 (사용자 / 물품)
    path("report/user/<int:user_pk>/", views.report_user, name="report_user"),
    path("report/listing/<int:listing_pk>/", views.report_listing, name="report_listing"),

    path("chats/", views.chat_list, name="chat_list"),
    #신고글 페이지
    path("reports/listings/", views.reported_listings, name="reported_listings"),


    # 채팅 기능
    path("chat/<int:room_id>/", views.chat_room, name="chat_room"),
    path("chat/start/<int:listing_pk>/", views.start_chat, name="start_chat"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
