import json
from django.core.management.base import BaseCommand
from api.models import Anime
import os
from django.conf import settings

DATA_DIR = os.path.join(settings.BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(DATA_DIR, "anime_data.json")

class Command(BaseCommand):
    Anime.objects.all().delete()
    def handle(self, *args, **kwargs):

        with open(OUTPUT_FILE, "r") as file:
            data = json.load(file)
        
            for item in data:
                Anime.objects.create(
                    name = item['name'],
                    desc = item['desc'],
                    studios = item['studios'],
                    genres = item['genres'],
                    popularity = item['popularity'],
                    score = item['score'],
                    img = item['img'],
                )