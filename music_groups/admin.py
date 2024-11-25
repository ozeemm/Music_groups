from django.contrib import admin
from music_groups.models import *

# Register your models here.
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["name", "user"] # Какие поля выводим в админку

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ["name", "group", "role", "user"]

@admin.register(MemberImage)
class MemberImageAdmin(admin.ModelAdmin):
    list_display = ["member", "image"]

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ["name", "year", "group", "genre", "image", "user"]

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ["name", "album", "user"]

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name", "user"]