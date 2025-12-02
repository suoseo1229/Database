# listings/admin.py

from django.contrib import admin
from .models import Listing, Report

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'status', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'reporter', 'reported_user', 'reported_listing', 'created_at')
    list_filter = ('report_type',)
    search_fields = ('reason',)

    # 신고된 게시글만 필터링하는 커스텀 뷰도 가능
