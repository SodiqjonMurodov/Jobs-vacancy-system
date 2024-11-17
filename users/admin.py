from django.contrib import admin
from .models import User, UserConfirmation

@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    list_display_links = ['id', 'username', 'email']


@admin.register(UserConfirmation)
class UserConfirmationModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'is_confirmed')
    list_display_links = ['id', 'code']
