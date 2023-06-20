import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import TitleGenre


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
            os.path.join(
                settings.BASE_DIR,
                "static", "data", "genre_title.csv"
            ),
            "r", encoding="utf-8"
        ) as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                TitleGenre.objects.create(
                    id=int(row[0]),
                    title_id=int(row[1]),
                    genre_id=int(row[2]),
                )
