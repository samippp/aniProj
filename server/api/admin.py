from django.contrib import admin
from .models import Anime, User, user_likedanime
# Register your models here.
admin.site.register(Anime)
admin.site.register(User)
admin.site.register(user_likedanime)