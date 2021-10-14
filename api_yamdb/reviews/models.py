from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField('Имя категории', max_length=256)
    slug = models.SlugField('Slug категории', max_length=150, unique=True)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ['id', ]


class Genre(models.Model):
    name = models.CharField('Имя жанра', max_length=256)
    slug = models.SlugField('Slug жанра', max_length=150, unique=True)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ['id', ]


class Title(models.Model):
    name = models.CharField(
        'Название произведения', max_length=256, unique=True
    )
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание произведения')
    genre = models.ManyToManyField(
        Genre, related_name='titles', help_text='Выберете жанр'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles',
        help_text='Выберете категорию', null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category', 'name', 'year']


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(
        default=5, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    text = models.TextField()
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_review_title'
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    text = models.TextField()
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )

    class Meta:
        ordering = ['-pub_date']
