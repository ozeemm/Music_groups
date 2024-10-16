from rest_framework import serializers
from music_groups.models import *

# Group
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

# Member
class MemberListSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)

    class Meta:
        model = Member
        fields = "__all__"

class MemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"

# Album
class AlbumListSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    genre = GroupSerializer(read_only=True)

    class Meta:
        model = Album
        fields = "__all__"

class AlbumCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"

# Song
class SongListSerializer(serializers.ModelSerializer):
    album = AlbumListSerializer(read_only=True)
    class Meta:
        model = Song
        fields = "__all__"

class SongCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = "__all__"

# Genre
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"