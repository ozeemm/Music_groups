import os
from django.core.management.base import BaseCommand
from django.conf import settings
from music_groups.models import Album, MemberImage

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        delete_counter = 0

        for dir, model in [("albums", Album), ("members", MemberImage)]:
            path = os.path.join(settings.MEDIA_ROOT, "music_groups", dir)

            for file in os.listdir(path):
                filePath = f"music_groups/{dir}/{file}"
                is_used = model.objects.filter(image=filePath).exists()

                if(not is_used):
                    fullPath = os.path.join(path, file)                    
                    os.remove(fullPath)

                    print("DELETED", filePath)
                    delete_counter += 1

        print(f"Deleted {delete_counter} images")
        
           