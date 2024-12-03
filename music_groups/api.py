from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count

from music_groups.models import *
from music_groups.serializers import *

class GroupsViewset(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin, 
    GenericViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if(not self.request.user.is_superuser):
            qs = qs.filter(user=self.request.user)

        return qs

class MembersViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Member.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return MemberListSerializer
        else:
            return MemberCreateSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if(not self.request.user.is_superuser):
            qs = qs.filter(user=self.request.user)

        return qs

class MemberImagesViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = MemberImage.objects.all()
    serializer_class = MemberImageSerializer

class AlbumsViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Album.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return AlbumListSerializer
        else:
            return AlbumCreateSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if(not self.request.user.is_superuser):
            qs = qs.filter(user=self.request.user)

        return qs

    class StatsSerializer(serializers.Serializer):
        albums_count = serializers.IntegerField()
        albums_by_groups = serializers.JSONField()
        albums_by_genres = serializers.JSONField()
        albums_by_years = serializers.JSONField()

    @action(detail=False, methods=['GET'], url_path='stats')
    def get_stats(self, request, *args, **kwargs):
        albums_count = Album.objects.aggregate(count=Count("*"))
        albums_by_groups = Album.objects.values('group__name').annotate(count=Count("group"))
        albums_by_genres = Album.objects.values('genre__name').annotate(count=Count("genre"))
        albums_by_years = Album.objects.values('year').annotate(count=Count("year"))

        stats = { 
            'albums_count': albums_count['count'], 
            'albums_by_groups': albums_by_groups, 
            'albums_by_genres': albums_by_genres, 
            'albums_by_years': albums_by_years
        }

        serializer = self.StatsSerializer(instance=stats)

        return Response(serializer.data)

class SongsViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Song.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return SongListSerializer
        else:
            return SongCreateSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        if(not self.request.user.is_superuser):
            qs = qs.filter(user=self.request.user)

        return qs
    
    class StatsSerializer(serializers.Serializer):
        songs_count = serializers.IntegerField()
        songs_by_albums = serializers.JSONField()

    @action(detail=False, methods=['GET'], url_path='stats')
    def get_stats(self, request, *args, **kwargs):
        songs_count = Song.objects.aggregate(count=Count("*"))
        songs_by_albums = Song.objects.values('album__name').annotate(count=Count("album"))

        stats = { 
            'songs_count': songs_count['count'], 
            'songs_by_albums': songs_by_albums
        }
        
        serializer = self.StatsSerializer(instance=stats)

        return Response(serializer.data)

class GenresViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if(not self.request.user.is_superuser):
            qs = qs.filter(user=self.request.user)

        return qs

class UserProfileViewset(GenericViewSet):
    @action(url_path="info", detail=False, methods=["GET"])
    def get_user(self, request, *args, **kwargs):
        user = request.user
        data = {"is_authenticated": user.is_authenticated}
        
        if user.is_authenticated:
            data.update({
                "is_superuser": user.is_superuser,
                "name": user.username
        })
        return Response(data)               