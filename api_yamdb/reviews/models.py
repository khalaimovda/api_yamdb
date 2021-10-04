from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Categories(models.Model):
    name = models.CharField('Имя категории', max_length=256)
    slug = models.SlugField('Тип категории', max_length=50, unique=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name
        super().save(*args, **kwargs)


class Genres(models.Model):
    name = models.CharField('Имя жанра', max_length=256)
    slug = models.SlugField('Тип жанра', max_length=50, unique=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name
        super().save(*args, **kwargs)


class Titles(models.Model):
    name = models.CharField(
        'Название произведения', max_length=256, unique=True
    )
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание произведения')
    genre = models.ManyToManyField(
        Genres, related_name='titles', help_text='Выберете жанр'
    )
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL, related_name='titles',
        help_text='Выберете категорию', null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category', 'name', 'year']


class Reviews(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(
        default=5, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    text = models.TextField()
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='reviews'
    )

    class Meta:
        ordering = ['-pub_date']


class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    text = models.TextField()
    review = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name='comments'
    )

    class Meta:
        ordering = ['-pub_date']
