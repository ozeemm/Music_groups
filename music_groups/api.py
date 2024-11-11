from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http.request import QueryDict

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

class MembersViewset(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Member.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return MemberListSerializer
        else:
            return MemberCreateSerializer
    
    def create(self, request, *args, **kwargs):
        member_data = QueryDict(mutable=True)
        member_data["name"] = request.data["name"]
        member_data["role"] = request.data["role"]
        member_data["group"] = request.data["group"]
        member_serializer = self.get_serializer_class()(data = member_data)
        if(member_serializer.is_valid()):
            created_member = member_serializer.save()
        
        for i in range(len(request.data) - len(member_data)):
            member_image_data = QueryDict(mutable=True)
            member_image_data["member"] = created_member.id
            member_image_data["image"] = request.data[f"image[{i}]"]
            member_image_serializer = MemberImageSerializer(data = member_image_data)
            if(member_image_serializer.is_valid()):
                member_image_serializer.save()

        return Response(status=201)

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

class SongsViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Song.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return SongListSerializer
        else:
            return SongCreateSerializer

class GenresViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

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