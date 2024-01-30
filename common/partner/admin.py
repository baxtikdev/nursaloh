from django.contrib import admin

from .models import Partner


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]
    exclude = ['created_at']
