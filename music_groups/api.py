from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Min, Max

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

    class StatsSerializer(serializers.Serializer):
        groups_count = serializers.IntegerField()

    @action(detail=False, methods=['GET'], url_path='stats')
    def get_stats(self, request, *args, **kwargs):
        groups_count = Group.objects.aggregate(groups_count=Count("*"))
        
        serializer = self.StatsSerializer(instance=groups_count)
        return Response(serializer.data)

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

    class StatsSerializer(serializers.Serializer):
        members_count = serializers.IntegerField()
        members_by_groups = serializers.JSONField()
        members_by_roles = serializers.JSONField()

    @action(detail=False, methods=['GET'], url_path='stats')
    def get_stats(self, request, *args, **kwargs):
        members_count = Member.objects.aggregate(
            count=Count("*")
        )
        members_by_groups = Member.objects.values('group__name').annotate(count=Count("group"))
        members_by_roles = Member.objects.values('role').annotate(count=Count("role"))

        stats = { 
            'members_count': members_count['count'], 
            'members_by_groups': members_by_groups, 
            'members_by_roles': members_by_roles
        }

        serializer = self.StatsSerializer(instance=stats)

        return Response(serializer.data)
    
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
        oldest_album_year = serializers.IntegerField()
        newest_album_year = serializers.IntegerField()
        albums_by_groups = serializers.JSONField()
        albums_by_genres = serializers.JSONField()
        albums_by_years = serializers.JSONField()

    @action(detail=False, methods=['GET'], url_path='stats')
    def get_stats(self, request, *args, **kwargs):
        int_stats = Album.objects.aggregate(
            count=Count("*"),
            min_year=Min("year"),
            max_year=Max("year")
        )
        albums_by_groups = Album.objects.values('group__name').annotate(count=Count("group"))
        albums_by_genres = Album.objects.values('genre__name').annotate(count=Count("genre"))
        albums_by_years = Album.objects.values('year').annotate(count=Count("year"))

        stats = { 
            'albums_count': int_stats['count'], 
            'oldest_album_year': int_stats['min_year'],
            'newest_album_year': int_stats['max_year'],
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
    
    class StatsSerializer(serializers.Serializer):
        genres_count = serializers.IntegerField()

    @action(detail=False, methods=['GET'], url_path='stats')
    def get_stats(self, request, *args, **kwargs):
        genres_count = Genre.objects.aggregate(genres_count=Count("*"))
        
        serializer = self.StatsSerializer(instance=genres_count)
        return Response(serializer.data)

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