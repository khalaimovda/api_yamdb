from django.urls import path, include
from rest_framework import routers

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
    UserViewSet,
    TokenObtainView,
    AuthSignupView,
)

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename=None)
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', TokenObtainView.as_view(), name='token_obtain_pair'),
    path('auth/signup/', AuthSignupView.as_view(), name='auth_signup')
]
