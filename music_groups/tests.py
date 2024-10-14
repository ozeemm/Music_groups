from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from music_groups.models import *

# Create your tests here.
class MembersViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        # Создание тестовых данных
        grp = baker.make("music_groups.Group")
        member = baker.make("music_groups.Member", group=grp)

		# Получение списка участников
        r = self.client.get('/api/members/')
        data = r.json()

		# Проверка данных участника
        assert member.id == data[0]['id']
        assert member.name == data[0]['name']
        assert member.role == data[0]['role']
        assert member.group.id == data[0]['group']['id']
        assert len(data) == 1

    def test_create_member(self):
        grp = baker.make("music_groups.Group")

		# Запрос на создание нового участника
        r = self.client.post("/api/members/", {
            "name": "some name",
            "group": grp.id,
            "role": "some role"
        })

		# id нового участника
        new_member_id = r.json()['id']

		# Проверка количества участников
        members = Member.objects.all()
        assert len(members) == 1

		# Првоерка совпадения данных участника
        new_member = Member.objects.filter(id=new_member_id).first()
        assert new_member.name == "some name"
        assert new_member.group == grp
        assert new_member.role == "some role"

    def test_delete_member(self):
	    # Создали 10 участников
        members = baker.make("music_groups.Member", 10) # 10 экземпляров
	
        # Проверили исходное количество
        r = self.client.get("/api/members/")
        data = r.json()
        assert len(data) == 10

		# Выбрали участника для удаления
        member_id_to_delete = members[3].id
        self.client.delete(f"/api/members/{member_id_to_delete}/")

		# Проверили, что количество участников уменьшилос
		# И выбранный участник удалён
        r = self.client.get("/api/members/")
        data = r.json()

        assert len(data) == 9
        assert member_id_to_delete not in [i['id'] for i in data]

    def test_update_member(self):
        # Создание 10 участников, выбор того, кого будем менять
        members = baker.make("music_groups.Member", 10)
        member: Member = members[2]

		# Проверка исходных имени и роли
        r = self.client.get(f"/api/members/{member.id}/")
        data = r.json()
        assert data["name"] == member.name
        assert data["role"] == member.role

		# Запрос на изменение
		# И проверка новых имени и роли из полученных данных в ответе
        r = self.client.put(f"/api/members/{member.id}/", {
            "name": "Other name",
            "role": "Other role"
        })
        data = r.json()
        assert data["name"] == "Other name"
        assert data["role"] == "Other role"

        # Проверка изменённых имени и роли в исходном объекте
        member.refresh_from_db() # Переподтянуть данные объекта из БД

        assert data["name"] == member.name
        assert data["role"] == member.role

class GroupsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_get_list(self):
        group = baker.make("music_groups.Group")

        r = self.client.get('/api/groups/')
        data = r.json()

        assert group.id == data[0]['id']
        assert group.name == data[0]['name']
        assert len(data) == 1

    def test_create_group(self):
        r = self.client.post("/api/groups/", {
            "name": "some group"
        })

        new_group_id = r.json()['id']

        groups = Group.objects.all()
        assert len(groups) == 1

        new_group = Group.objects.filter(id=new_group_id).first()
        assert new_group.name == "some group"

    def test_delete_group(self):
        groups = baker.make("music_groups.Group", 10)
	
        r = self.client.get("/api/groups/")
        data = r.json()
        assert len(data) == 10

        group_id_to_delete = groups[3].id
        self.client.delete(f"/api/groups/{group_id_to_delete}/")

        r = self.client.get("/api/groups/")
        data = r.json()

        assert len(data) == 9
        assert group_id_to_delete not in [i['id'] for i in data]

    def test_update_group(self):
        groups = baker.make("music_groups.Group", 10)
        group: Group = groups[2]

        r = self.client.get(f"/api/groups/{group.id}/")
        data = r.json()
        assert data["name"] == group.name

        r = self.client.put(f"/api/groups/{group.id}/", {
            "name": "Other group",
        })
        data = r.json()
        assert data["name"] == "Other group"

        group.refresh_from_db()

        assert data["name"] == group.name

class AlbumsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_get_list(self):
        grp = baker.make("music_groups.Group")
        gnr = baker.make("music_groups.Genre")

        album = baker.make("music_groups.Album", group=grp, genre=gnr)

        r = self.client.get('/api/albums/')
        data = r.json()

        assert album.id == data[0]['id']
        assert album.name == data[0]['name']
        assert album.year == data[0]['year']
        assert album.group.id == data[0]['group']['id']
        assert album.genre.id == data[0]['genre']['id']
        assert len(data) == 1

    def test_create_album(self):
        r = self.client.post("/api/albums/", {
            "name": "some album",
            "year": 1900
        })

        new_album_id = r.json()['id']

        albums = Album.objects.all()
        assert len(albums) == 1

        new_album = Album.objects.filter(id=new_album_id).first()
        assert new_album.name == "some album"
        assert new_album.year == 1900

    def test_delete_album(self):
        albums = baker.make("music_groups.Album", 10)
	
        r = self.client.get("/api/albums/")
        data = r.json()
        assert len(data) == 10

        album_id_to_delete = albums[3].id
        self.client.delete(f"/api/albums/{album_id_to_delete}/")

        r = self.client.get("/api/albums/")
        data = r.json()

        assert len(data) == 9
        assert album_id_to_delete not in [i['id'] for i in data]
        

    def test_update_album(self):
        albums = baker.make("music_groups.Album", 10)
        album: Album = albums[2]

        r = self.client.get(f"/api/albums/{album.id}/")
        data = r.json()
        assert data["name"] == album.name

        r = self.client.put(f"/api/albums/{album.id}/", {
            "name": "Other album",
            "year": 1900
        })
        data = r.json()
        assert data["name"] == "Other album"
        assert data["year"] == 1900

        album.refresh_from_db()

        assert data["name"] == album.name
        assert data["year"] == album.year

class SongsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_get_list(self):
        albm = baker.make("music_groups.Album")

        song = baker.make("music_groups.Song", album=albm)

        r = self.client.get('/api/songs/')
        data = r.json()

        assert song.id == data[0]['id']
        assert song.name == data[0]['name']
        assert song.album.id == data[0]['album']['id']
        assert len(data) == 1

    def test_create_song(self):
        r = self.client.post("/api/songs/", {
            "name": "some song",
        })

        new_song_id = r.json()['id']

        songs = Song.objects.all()
        assert len(songs) == 1

        new_album = Song.objects.filter(id=new_song_id).first()
        assert new_album.name == "some song"

    def test_delete_song(self):
        songs = baker.make("music_groups.Song", 10)
	
        r = self.client.get("/api/songs/")
        data = r.json()
        assert len(data) == 10

        song_id_to_delete = songs[3].id
        self.client.delete(f"/api/songs/{song_id_to_delete}/")

        r = self.client.get("/api/songs/")
        data = r.json()

        assert len(data) == 9
        assert song_id_to_delete not in [i['id'] for i in data]

    def test_update_song(self):
        songs = baker.make("music_groups.Song", 10)
        song: Song = songs[2]

        r = self.client.get(f"/api/songs/{song.id}/")
        data = r.json()
        assert data["name"] == song.name

        r = self.client.put(f"/api/songs/{song.id}/", {
            "name": "Other song",
        })
        data = r.json()
        assert data["name"] == "Other song"

        song.refresh_from_db()
        assert data["name"] == song.name

class GenresViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_get_list(self):
        genre = baker.make("music_groups.Genre")

        r = self.client.get('/api/genres/')
        data = r.json()

        assert genre.id == data[0]['id']
        assert genre.name == data[0]['name']
        assert len(data) == 1

    def test_create_genre(self):
        r = self.client.post("/api/genres/", {
            "name": "some group"
        })

        new_genre_id = r.json()['id']

        genres = Genre.objects.all()
        assert len(genres) == 1

        new_genre = Genre.objects.filter(id=new_genre_id).first()
        assert new_genre.name == "some group"

    def test_delete_genre(self):
        genres = baker.make("music_groups.Genre", 10)
	
        r = self.client.get("/api/genres/")
        data = r.json()
        assert len(data) == 10

        genre_id_to_delete = genres[3].id
        self.client.delete(f"/api/genres/{genre_id_to_delete}/")

        r = self.client.get("/api/genres/")
        data = r.json()

        assert len(data) == 9
        assert genre_id_to_delete not in [i['id'] for i in data]

    def test_update_genre(self):
        genres = baker.make("music_groups.Genre", 10)
        genre: Genre = genres[2]

        r = self.client.get(f"/api/genres/{genre.id}/")
        data = r.json()
        assert data["name"] == genre.name

        r = self.client.put(f"/api/genres/{genre.id}/", {
            "name": "Other genre",
        })
        data = r.json()
        assert data["name"] == "Other genre"

        genre.refresh_from_db()

        assert data["name"] == genre.name