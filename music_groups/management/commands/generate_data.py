from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from music_groups.models import *
from faker import Faker
from random import randint, choice

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        min_groups = 15
        max_groups = 40

        min_members_in_group = 2
        max_members_in_group = 5
        
        min_albums_for_group = 1
        max_albums_for_group = 7
        
        min_songs_in_album = 3
        max_songs_in_album = 12
        
        print_each = 5

        admin = User.objects.filter(id = 1)[0]

        roles = [
            "Вокал", 
            "Гитара", 
            "Бас-гитара", 
            "Барабаны", 
            "Синтезатор", 
            "Фортепиано", 
            "Рояль", 
            "Скрипка",
            "Виолончель",
            "Контрабас",
            "Треугольник",
            "Балалайка",
            "Гусли",
            "Флейта",
            "Саксофон",
            "Труба",
            "Тромбон",
            "Дудка",
            "Гармошка",
            "Аккордеон",
            "Баян",
            "Спецэффекты",
            "DJ",
            "Укулеле"
        ]
        
        fake = Faker(['ru_RU', 'en_US'])

        groups_created = 0
        memebers_created = 0
        albums_created = 0
        songs_created = 0

        for _ in range(randint(min_groups, max_groups)):
            if(_ % print_each == 0 and _ != 0):
                print(f"{_} groups created!")

            group = Group(name = self.rand_object_name(fake), user=admin)
            group.save()
            groups_created += 1

            members_count = randint(min_members_in_group, max_members_in_group)
            for i in range(members_count):
                member = Member(name=fake.name(), role=choice(roles), group=group, user=admin)
                member.save()
                memebers_created += 1
            
            for i in range(min_albums_for_group, max_albums_for_group):
                year = randint(1964, 2024)
                genre = choice(Genre.objects.all())

                album = Album(name=self.rand_object_name(fake), year=year, group=group, genre=genre, user=admin)
                album.save()
                albums_created += 1

                for j in range(min_songs_in_album, max_songs_in_album):
                    song = Song(name=self.rand_object_name(fake), album=album, user=admin)
                    song.save()
                    songs_created += 1
        
        print(f"Groups created: {groups_created}; Total: {len(Group.objects.all())}")
        print(f"Members created: {memebers_created}; Total: {len(Member.objects.all())}")
        print(f"Albums created: {albums_created}; Total: {len(Album.objects.all())}")
        print(f"Songs created: {songs_created}; Total: {len(Song.objects.all())}")
        
    def rand_object_name(self, fake):
        name = ""
        rand = randint(0, 3)
        if(rand == 0): name = fake.city_name()
        elif(rand == 1): name = fake.file_name()
        elif(rand == 2): name = fake.job()
        elif(rand == 3): name = fake.street_name()

        return name        