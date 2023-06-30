import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
            os.path.join(
                settings.BASE_DIR,
                "static", "data", "category.csv"
            ),
            "r", encoding="utf-8"
        ) as file:
            reader = csv.reader(file, delimiter=",")
            next(reader, None)
            for row in reader:
                Category.objects.create(
                    id=int(row[0]),
                    name=row[1],
                    slug=row[2],
                )
