"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

from music_groups import views
from music_groups.api import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("groups", GroupsViewset, basename="groups")
router.register("members", MembersViewset, basename="members")
router.register("albums", AlbumsViewset, basename="albums")
router.register("songs", SongsViewset, basename="songs")
router.register("genres", GenresViewset, basename="genres")
router.register("member_images", MemberImagesViewset, basename="member_images")
router.register("user", UserProfileViewset, basename="user")
router.register("export", ExportViewset, basename="export")

urlpatterns = [
    path('', views.ShowGroupsView.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
