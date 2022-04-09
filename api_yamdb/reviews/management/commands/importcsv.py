import csv

from django.core.management.base import BaseCommand

from api_yamdb.settings import BASE_DIR
from reviews.models import (Category, Comments, Genre, Review, Title,
                            TitlesGenres, User)

FILES = [
    f'{BASE_DIR}\\static\\data\\category.csv',
    f'{BASE_DIR}\\static\\data\\titles.csv',
    f'{BASE_DIR}\\static\\data\\genre.csv',
    f'{BASE_DIR}\\static\\data\\genre_title.csv',
    f'{BASE_DIR}\\static\\data\\users.csv',
    f'{BASE_DIR}\\static\\data\\review.csv',
    f'{BASE_DIR}\\static\\data\\comments.csv',
]


class Command(BaseCommand):
    help = 'Import CSV files'

    def handle(self, *args, **options):
        for file in FILES:
            if 'category.csv' in file:
                table = csv.reader(
                    open(file, encoding='utf-8'), delimiter=','
                )
                Category.objects.bulk_create(
                    Category(
                        id=int(row[0]),
                        name=row[1],
                        slug=row[2]
                    ) for row in list(table)[1:]
                )
            elif 'titles.csv' in file:
                table = csv.reader(
                    open(file, encoding='utf-8'), delimiter=','
                )
                Title.objects.bulk_create(
                    Title(
                        id=int(row[0]),
                        name=row[1],
                        year=row[2],
                        category=Category.objects.get(id=int(row[3]))
                    ) for row in list(table)[1:]
                )
            elif 'genre.csv' in file:
                table = csv.reader(
                    open(file, encoding='utf-8'), delimiter=','
                )
                Genre.objects.bulk_create(
                    Genre(
                        id=int(row[0]),
                        name=row[1],
                        slug=row[2]
                    ) for row in list(table)[1:]
                )
            elif 'genre_title.csv' in file:
                table = csv.reader(
                    open(file, encoding='utf-8'), delimiter=','
                )
                TitlesGenres.objects.bulk_create(
                    TitlesGenres(
                        id=int(row[0]),
                        title=Title.objects.get(id=int(row[1])),
                        genre=Genre.objects.get(id=int(row[2])),
                    ) for row in list(table)[1:]
                )
            elif 'users.csv' in file:
                table = csv.reader(
                    open(file, encoding='utf-8'), delimiter=','
                )
                User.objects.bulk_create(
                    User(
                        id=int(row[0]),
                        username=row[1],
                        email=row[2],
                        role=row[3],
                        bio=row[4],
                        first_name=row[5],
                        last_name=row[6]
                    ) for row in list(table)[1:]
                )
            elif 'review.csv' in file:
                table = csv.reader(
                    open(file, encoding='utf-8'), delimiter=','
                )
                Review.objects.bulk_create(
                    Review(
                        id=int(row[0]),
                        title=Title.objects.get(id=int(row[1])),
                        text=row[2],
                        author=User.objects.get(id=int(row[3])),
                        score=int(row[4]),
                        pub_date=row[5]
                    ) for row in list(table)[1:]
                )
            elif 'comments.csv' in file:
                table = csv.reader(
                    open(file, encoding='utf-8'), delimiter=','
                )
                Comments.objects.bulk_create(
                    Comments(
                        id=int(row[0]),
                        review=Review.objects.get(id=int(row[1])),
                        text=row[2],
                        author=User.objects.get(id=int(row[3])),
                        pub_date=row[4]
                    ) for row in list(table)[1:]
                )
            else:
                print('Такой таблицы нет в базе данных')
