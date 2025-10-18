from django.contrib import admin
from .models import CustomUserModel

@admin.register(CustomUserModel)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'role')
    ordering = ('username',)
