from django.contrib import admin
from .models import Guest


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    """
    Customizes how the Guest model is displayed in the Django admin.
    """
    list_display = ('name', 'phone_number', 'status', 'will_attend', 'created_at')
    list_filter = ('status', 'will_attend')
    search_fields = ('name', 'phone_number', 'unique_id')
    readonly_fields = ('unique_id', 'created_at')
