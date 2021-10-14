from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role', )
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role', )
        read_only_fields = ('role', )
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'bio': {'required': False},
        }


class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['view'].kwargs['title_id']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        model = Review
        read_only_fields = ('id', 'author', 'pub_date', 'title')

    def validate(self, data):
        data = super().validate(data)
        if self._kwargs['context']['action'] == 'create':
            user = self._kwargs['context']['user']
            title = self._kwargs['context']['title']
            if Review.objects.filter(
                author=user, title=title
            ).exists():
                raise serializers.ValidationError(
                    'На одно произведение пользователь'
                    'может оставить только один отзыв')
        return data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug', )
        model = Category
        extra_kwargs = {
            'name': {'required': True},
            'slug': {'required': True},
        }


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug', )
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    # С DecimalField не проходит тесты
    # rating = serializers.DecimalField(
    #     max_digits=4, decimal_places=2, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title


class TitleCreateUpdateSerializer(TitleReadSerializer):
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего')
        return value


class TokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[UnicodeUsernameValidator()], )
    confirmation_code = serializers.CharField(max_length=30)


class AuthSignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True, max_length=254)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('"me" is forbidden username')
        return value
