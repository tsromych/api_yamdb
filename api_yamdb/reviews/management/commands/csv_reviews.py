import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Review


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
            os.path.join(
                settings.BASE_DIR,
                'static', 'data', 'review.csv'
            ),
            'r', encoding='utf-8'
        ) as f:
            csv_reader = csv.reader(f, delimiter=';')
            for row in csv_reader:
                Review.objects.create(id=row[0], title_id=int(row[1]),
                                      text=row[2], author_id=int(row[3]),
                                      score=int(row[4]), pub_date=row[5])
