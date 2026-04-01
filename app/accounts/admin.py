from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nik', 'bagian', 'branch', 'line', 'rfid_user')
    search_fields = ('user__username', 'nik', 'rfid_user', 'user__first_name')