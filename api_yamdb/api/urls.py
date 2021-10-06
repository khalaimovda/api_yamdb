from django.urls import path, include
from rest_framework import routers

from .views import (
    CategoriesViewSet,
    GenresViewSet,
    TitlesViewSet,
    ReviewsViewSet,
    CommentsViewSet,
    UserViewSet,
    TokenObtainView,
    AuthSignupView,
)

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename=None)
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'genres', GenresViewSet, basename='genres')
router.register(r'titles', TitlesViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', TokenObtainView.as_view(), name='token_obtain_pair'),
    path('auth/signup/', AuthSignupView.as_view(), name='auth_signup')
]
