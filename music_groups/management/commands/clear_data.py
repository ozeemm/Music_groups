from django.core.management.base import BaseCommand
from music_groups.models import *

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Group.objects.all().delete()
        Album.objects.all().delete()
        
           