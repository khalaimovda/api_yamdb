from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from drf_yasg.utils import swagger_auto_schema

from reviews.models import Categories, Genres, Titles, Reviews, Comments
from .serializers import (
    CategoriesSerializer, GenresSerializer, TitlesSerializer,
    ReviewsSerializer, CommentsSerializer, UserSerializer,
    TokenObtainSerializer, AuthSignupSerializer,
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


class AuthSignupView(APIView):
    permission_classes = ()

    @swagger_auto_schema(
        request_body=AuthSignupSerializer
    )
    def post(self, request):
        serializer = AuthSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get_or_create(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
            )[0]

            new_password = user.get_new_password()

            send_mail(
                'Yamdb. Код подтверждения.',
                'Вы зарегистрировались на ресурсе Yamdb.\n'
                f'username = {serializer.validated_data["username"]}\n'
                f'confirmation_code = {new_password}',
                'yamdb@example.com',
                [serializer.validated_data['email']],
                fail_silently=False,
            )

            user.set_password(new_password)
            user.save()

            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
