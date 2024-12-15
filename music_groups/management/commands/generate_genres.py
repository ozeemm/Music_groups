from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from music_groups.models import Genre
import json

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        admin = User.objects.filter(id = 1)[0]

        with open("./music_groups/management/commands/genres.json", "r") as file:
            data = file.read()
            json_data = json.loads(data)
            printable = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
            for key in json_data.keys():
                if('.v2' in key):
                    continue
                key = ''.join(filter(lambda x: x in printable, key))
                while('  ' in key):
                    key = key.replace('  ', ' ')
                key = key.title()

                Genre.objects.create(name = key, user = admin)

            print(f"Genres: {len(Genre.objects.all())}")        
        
           