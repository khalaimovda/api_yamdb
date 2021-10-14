from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title
from .filters import TitleFilter
from .permissions import (IsAuthorOrModeratorOrAdminOrSuperuser,
                          IsSuperuserOrAdmin, IsSuperuserOrAdminOrReadOnly)
from .serializers import (AuthSignupSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer, ReviewSerializer,
                          TitleCreateUpdateSerializer, TitleReadSerializer,
                          TokenObtainSerializer, UserMeSerializer,
                          UserSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated, IsSuperuserOrAdmin]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    lookup_field = 'username'
    lookup_url_kwarg = 'username'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserMeSerializer,
        filter_backends=(),
        pagination_class=None
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsSuperuserOrAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_url_kwarg = 'slug'
    lookup_field = 'slug'


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsSuperuserOrAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_url_kwarg = 'slug'
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('category', 'name', 'year')
    permission_classes = (IsSuperuserOrAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter
    lookup_url_kwarg = 'titles_id'

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleCreateUpdateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    lookup_url_kwarg = 'review_id'

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            permission_classes = (IsAuthorOrModeratorOrAdminOrSuperuser, )
        else:
            permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        context.update({
            'action': self.action,
            'title': title,
            'user': self.request.user
        })
        return context


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            permission_classes = (IsAuthorOrModeratorOrAdminOrSuperuser, )
        else:
            permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'],
                                   title_id=self.kwargs['title_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'],
                                   title_id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, review=review)


class TokenObtainView(APIView):
    permission_classes = ()

    @swagger_auto_schema(
        request_body=TokenObtainSerializer
    )
    def post(self, request):
        serializer = TokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(klass=User, username=request.data['username'])

        if not default_token_generator.check_token(
            user, request.data['confirmation_code']
        ):
            raise ValidationError(detail='Confirmation code is incorrect')

        refresh = RefreshToken.for_user(user=user)
        data = {'token': str(refresh.access_token)}
        return Response(status=status.HTTP_200_OK, data=data)


@api_view(http_method_names=['POST', ],)
@permission_classes([])
def auth_signup(request):
    serializer = AuthSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user = User.objects.get_or_create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
        )[0]
    except IntegrityError as e:
        return Response(data=repr(e), status=status.HTTP_400_BAD_REQUEST)

    confirmation_code = default_token_generator.make_token(user)

    send_mail(
        'Yamdb. Код подтверждения.',
        'Вы зарегистрировались на ресурсе Yamdb.\n'
        f'username = {serializer.validated_data["username"]}\n'
        f'confirmation_code = {confirmation_code}',
        'yamdb@example.com',
        [serializer.validated_data['email']],
        fail_silently=False,
    )

    user.save()
    return Response(data=serializer.data, status=status.HTTP_200_OK)
