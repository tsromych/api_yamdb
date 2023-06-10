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
                'static', 'data', 'comments.csv'
            ),
            'r', encoding='utf-8'
        ) as f:
            csv_reader = csv.reader(f, delimiter=';')
            for row in csv_reader:
                Comments.objects.create(id=int(row[0]), review_id=int(row[1]),
                                        text=row[2], author_id=int(row[3]),
                                        pub_date=row[4])
