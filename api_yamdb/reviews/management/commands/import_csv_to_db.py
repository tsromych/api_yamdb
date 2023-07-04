import os
from csv import DictReader

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from users.models import CustomUser

parent_dir = os.path.join(settings.BASE_DIR, 'static', 'data/')
file_name = {
    'users': 'users.csv',
    'category': 'category.csv',
    'genre': 'genre.csv',
    'titles': 'titles.csv',
    'genre_title': 'genre_title.csv',
    'review': 'review.csv',
    'comments': 'comments.csv',
}


class Command(BaseCommand):
    """Загрузка данных из CSV файлов в базу данных."""
    def handle(self, *args, **options):
        def print_import_status(file_name):
            print(self.style.SUCCESS('Импорт данных из файла '
                                     f'{file_name} завершен!'))

        print(self.style.SUCCESS('Начинем загрузку данных из CSV файлов...'))
        with open(
            parent_dir + file_name['users'], mode='r', encoding='utf-8'
        ) as file:
            reader = DictReader(file)
            for row in reader:
                CustomUser.objects.create(
                    id=int(row['id']),
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=['first_name'],
                    last_name=['last_name'],
                )
            print_import_status(file_name['users'])

        with open(
            parent_dir + file_name['category'], mode='r', encoding='utf-8'
        ) as file:
            reader = DictReader(file)
            for row in reader:
                Category.objects.create(
                    id=int(row['id']),
                    name=row['name'],
                    slug=row['slug'],
                )
            print_import_status(file_name['category'])

        with open(
            parent_dir + file_name['genre'], mode='r', encoding='utf-8'
        ) as file:
            reader = DictReader(file)
            for row in reader:
                Genre.objects.create(
                    id=int(row['id']),
                    name=row['name'],
                    slug=row['slug'],
                )
            print_import_status(file_name['genre'])

        with open(
            parent_dir + file_name['titles'], mode='r', encoding='utf-8'
        ) as file:
            reader = DictReader(file)
            for row in reader:
                Title.objects.create(
                    id=int(row['id']),
                    name=row['name'],
                    year=int(row['year']),
                    category_id=int(row['category']),
                )
            print_import_status(file_name['titles'])

        with open(
            parent_dir + file_name['genre_title'], mode='r', encoding='utf-8'
        ) as file:
            reader = DictReader(file)
            for row in reader:
                TitleGenre.objects.create(
                    id=int(row['id']),
                    title_id=int(row['title_id']),
                    genre_id=int(row['genre_id']),
                )
            print_import_status(file_name['genre_title'])

        with open(
            parent_dir + file_name['review'], mode='r', encoding='utf-8'
        ) as file:
            reader = DictReader(file)
            for row in reader:
                Review.objects.create(
                    id=int(row['id']),
                    title_id=int(row['title_id']),
                    text=row['text'],
                    author_id=int(row['author']),
                    score=int(row['score']),
                    pub_date=row['pub_date'],
                )
            print_import_status(file_name['review'])

        with open(
            parent_dir + file_name['comments'], mode='r', encoding='utf-8'
        ) as file:
            reader = DictReader(file)
            for row in reader:
                Comment.objects.create(
                    id=int(row['id']),
                    text=row['text'],
                    pub_date=row['pub_date'],
                    author_id=int(row['author']),
                    review_id=int(row['review_id']),
                )
            print_import_status(file_name['comments'])

        print(self.style.SUCCESS('Загрузка данных завершена'))
