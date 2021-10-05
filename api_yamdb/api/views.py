from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenViewBase

from reviews.models import Categories, Genres, Titles, Reviews, Comments
from .serializers import (
    CategoriesSerializer, GenresSerializer, TitlesSerializer,
    ReviewsSerializer, CommentsSerializer, UserSerializer,
    TokenObtainSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class TokenObtainView(TokenViewBase):
    serializer_class = TokenObtainSerializer
