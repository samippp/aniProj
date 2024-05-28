import json
from django.core.management.base import BaseCommand
from api.models import anime

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open(r'C:\Users\samip\Documents\aniProj\anime_data.json') as file:
            data = json.load(file)

            for item in data:
                anime.objects.create(
                    name = item['name'],
                    studios = item['studios'],
                    genres = item['genres'],
                    popularity = item['popularity'],
                    score = item['score'],
                    img = item['img'],
                )