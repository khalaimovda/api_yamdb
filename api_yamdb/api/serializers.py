from rest_framework import serializers

from ..reviews.models import Categories, Genres, Titles, Reviews, Comments


class CommentsSerializer(serializers.ModelSerializer):
    pass


class ReviewsSerializer(serializers.ModelSerializer):
    pass


class CategoriesSerializer(serializers.ModelSerializer):
    pass


class GenresSerializer(serializers.ModelSerializer):
    pass


class TitlesSerializer(serializers.ModelSerializer):
    pass
