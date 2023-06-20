import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Comments


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
            os.path.join(
                settings.BASE_DIR,
                "static", "data", "comments.csv"
            ),
            "r", encoding="utf-8"
        ) as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                Comments.objects.create(
                    id=int(row[0]),
                    review_id=int(row[1]),
                    text=row[2],
                    author=int(row[3]),
                    pub_date=row[4],
                )
