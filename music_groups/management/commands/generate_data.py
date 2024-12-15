import os
from django.core.management.base import BaseCommand
from music_groups.models import *
from faker import Faker

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        fake = Faker(['ru_RU', 'en_US'])

        # Для названий (группы/альбома/песни):
        # fake.street_name()
        # fake.file_name()

        # Жанры погуглить самому
        
        
           