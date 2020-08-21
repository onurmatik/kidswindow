from django.contrib import admin
from .models import Profile, ProfileGame


@admin.register(ProfileGame)
class ProfileLanguageAdmin(admin.ModelAdmin):
    list_display = ['profile', 'game', 'tutor']


class ProfileGameInline(admin.TabularInline):
    model = ProfileGame
    extra = 0


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_confirmed', 'timezone']
    inlines = [ProfileGameInline]
