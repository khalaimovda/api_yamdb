import csv
import os
from typing import Union

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import ObjectDoesNotExist
from django.db.utils import DatabaseError

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class Command(BaseCommand):
    help = """This script loads data from files
    ('category.csv', 'comments.csv', 'genre.csv', 'genre_title.csv',
     'review.csv', 'titles.csv', 'users.csv')
    from directory = STATICFILES_DIRS[0]/data/ to
    corresponding models ( Category, Comment, Genre, Review, Title, User )"""

    CSV_DIRECTORY_PATH = (
        os.path.join(settings.STATICFILES_DIRS[0], 'data/'),)[0]

    def handle(self, *args, **options):
        # User
        file_path = (
            os.path.join(self.CSV_DIRECTORY_PATH, 'users.csv'),)[0]
        self.load_data_from_file_to_model(file_path=file_path, model=User)

        # Category
        file_path = (
            os.path.join(self.CSV_DIRECTORY_PATH, 'category.csv'),)[0]
        self.load_data_from_file_to_model(file_path=file_path, model=Category)

        # Genre
        file_path = (
            os.path.join(self.CSV_DIRECTORY_PATH, 'genre.csv'),)[0]
        self.load_data_from_file_to_model(file_path=file_path, model=Genre)

        # Title
        file_path = (
            os.path.join(self.CSV_DIRECTORY_PATH, 'titles.csv'),)[0]
        self.load_data_from_file_to_model(file_path=file_path, model=Title)

        # Title and Genre ManyToMany
        file_path = (
            os.path.join(self.CSV_DIRECTORY_PATH, 'genre_title.csv'),)[0]
        self.load_genre_title(file_path=file_path)

        # Review
        file_path = (
            os.path.join(self.CSV_DIRECTORY_PATH, 'review.csv'),)[0]
        self.load_data_from_file_to_model(file_path=file_path, model=Review)

        # Comment
        file_path = (
            os.path.join(self.CSV_DIRECTORY_PATH, 'comments.csv'),)[0]
        self.load_data_from_file_to_model(file_path=file_path, model=Comment)

    def load_data_from_file_to_model(
        self,
        file_path: str,
        model: Union[Category, Genre, Title, Review, Comment, User]
    ):
        self.stdout.write('##########################################')
        self.stdout.write(f'Model: {model.__name__}')
        self.stdout.write('##########################################')
        try:
            f = open(file=file_path, encoding='utf-8')
        except FileNotFoundError:
            self.stdout.write(f'CSV file {file_path} not found')
        else:
            reader = csv.reader(f)
            header_row = next(reader)
            try:
                for name in header_row:
                    getattr(model, name)
            except AttributeError:
                self.stderr.write(f'There are incorrect field names in'
                                  f' {file_path}. Migration canceled.')
            else:
                for row in reader:
                    self.stdout.write('')
                    data = {header_row[i]: row[i] for i in range(0, len(row))}
                    self.stdout.write(f'data = {data}')
                    if model.objects.filter(id=data['id']).exists():
                        self.stdout.write(f'Object with id = {data["id"]}'
                                          ' already exists')
                        continue
                    try:
                        model.objects.create(**data)
                    except DatabaseError as error:
                        self.stdout.write('DatabaseError. Object not created')
                        self.print_err(error)
                    else:
                        self.stdout.write('Object created')
            finally:
                self.stdout.write('##########################################')
                self.stdout.write('')

            f.close()

    def load_genre_title(self, file_path: str):
        self.stdout.write('##########################################')
        self.stdout.write('Model: Title and Genre ManyToMany')
        self.stdout.write('##########################################')
        try:
            f = open(file=file_path, encoding='utf-8')
        except FileNotFoundError:
            self.stdout.write(f'CSV file {file_path} not found')
        else:
            reader = csv.reader(f)
            header_row = next(reader)
            try:
                assert len(header_row) == 3, 'Parameter count <> 3'
                assert header_row[0] == 'id', 'First parameter name <> "id"'
                assert header_row[1] == 'title_id', ('Second parameter name'
                                                     ' <> "title_id"')
                assert header_row[2] == 'genre_id', ('First parameter name'
                                                     ' <> "genre_id"')
            except AssertionError as error:
                self.stdout.write(f'CSV file {file_path} is incorrect')
                self.print_err(error)

            else:

                for row in reader:
                    self.stdout.write('')
                    data = {header_row[i]: row[i] for i in range(0, len(row))}
                    self.stdout.write(f'data = {data}')
                    id, title_id, genre_id = map(int, row)  # noqa
                    try:
                        title = Title.objects.get(pk=title_id)
                        genre = Genre.objects.get(pk=genre_id)
                    except ObjectDoesNotExist as error:
                        self.stdout.write('Incorrect object id.'
                                          'Object not found')
                        self.print_err(error)
                    else:
                        if title.genre.filter(id=genre_id):
                            self.stdout.write('This relation already exists')
                        else:
                            title.genre.add(genre)
                            self.stdout.write('Relation successfully set')
            finally:
                self.stdout.write('##########################################')
                self.stdout.write('')

            f.close()

    def print_err(self, error):
        self.stdout.write(getattr(error, 'message', repr(error)))
