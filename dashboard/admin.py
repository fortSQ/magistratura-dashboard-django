from django.contrib import admin
from .models import UserProfile, Widget

admin.site.register([
    UserProfile,
    Widget
])
