import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
            os.path.join(
                settings.BASE_DIR,
                'static', 'data', 'users.csv'
            ),
            'r', encoding='utf-8'
        ) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                User.objects.create(id=int(row[0]), username=row[1],
                                    email=row[2], role=row[3])
