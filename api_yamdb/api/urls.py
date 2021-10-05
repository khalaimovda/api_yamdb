from django.urls import path, include
from rest_framework import routers

from .views import (CategoriesViewSet, GenresViewSet, TitlesViewSet,
                    ReviewsViewSet, CommentsViewSet
                    )


router = routers.DefaultRouter()
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'genres', GenresViewSet, basename='genres')
router.register(r'titles', TitlesViewSet, basename='titles')
router.register(
    r'titles/(?P<id>\d+)/reviews', ReviewsViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<id>\d+)/reviews/(?P<id>\d+)/comments',
    CommentsViewSet, basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
]
