from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from music_groups.models import *

# Create your tests here.
class MembersViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        grp = baker.make("music_groups.Group")
        member = baker.make("music_groups.Member", group=grp)

        r = self.client.get('/api/members/')
        data = r.json()

        assert member.id == data[0]['id']
        assert member.name == data[0]['name']
        assert member.role == data[0]['role']
        assert member.group.id == data[0]['group']['id']
        assert len(data) == 1

    def test_create_member(self):
        grp = baker.make("music_groups.Group")

        r = self.client.post("/api/members/", {
            "name": "some name",
            "group": grp.id,
            "role": "some role"
        })

        new_member_id = r.json()['id']

        members = Member.objects.all()
        assert len(members) == 1

        new_member = Member.objects.filter(id=new_member_id).first()
        assert new_member.name == "some name"
        assert new_member.group == grp
        assert new_member.role == "some role"

    def test_delete_member(self):
        members = baker.make("music_groups.Member", 10) # 10 экземпляров
        
        r = self.client.get("/api/members/")
        data = r.json()
        assert len(data) == 10

        member_id_to_delete = members[3].id
        self.client.delete(f"/api/members/{member_id_to_delete}/")

        r = self.client.get("/api/members/")
        data = r.json()
        
        assert len(data) == 9
        assert member_id_to_delete not in [i['id'] for i in data]

    def test_update_member(self):
        members = baker.make("music_groups.Member", 10)
        member: Member = members[2]

        r = self.client.get(f"/api/members/{member.id}/")
        data = r.json()
        assert data["name"] == member.name
        assert data["role"] == member.role

        r = self.client.put(f"/api/members/{member.id}/", {
            "name": "Other name",
            "role": "Other role"
        })
        data = r.json()
        assert data["name"] == "Other name"
        assert data["role"] == "Other role"

        # Переподтянуть данные объекта из БД
        member.refresh_from_db()

        assert data["name"] == member.name
        assert data["role"] == member.role