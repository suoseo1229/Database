from django.contrib import admin
from .models import Listing, Report, ChatRoom

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'status', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'reporter', 'reported_user', 'reported_listing', 'created_at')
    list_filter = ('report_type',)
    search_fields = ('reason',)

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('listing', 'seller', 'buyer', 'is_closed', 'created_at')
    list_filter = ('is_closed',)
    search_fields = ('listing__title', 'seller__username', 'buyer__username')
