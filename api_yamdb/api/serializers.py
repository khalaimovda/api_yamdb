from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Categories, Comments, Genres, Reviews, Titles

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

    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role', )
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


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='id'
    )

    class Meta:
        fields = '__all__'
        model = Comments


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='id',
        default=CurrentTitleDefault()
    )

    class Meta:
        fields = '__all__'
        model = Reviews
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Reviews.objects.all(), fields=('author', 'title')
            )
        ]


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Categories


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Titles


class TokenObtainSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD
    password_field = settings.PASSWORD_FIELD

    default_error_messages = {
        'no_active_account': _(
            'No active account found with the given credentials'
        )
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields[self.password_field] = PasswordField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs[self.password_field],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        get_object_or_404(
            klass=User,
            username=attrs[self.username_field]
        )

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.ValidationError(
                detail=self.error_messages['no_active_account'],
            )

        refresh = self.get_token(self.user)
        data = {'token': str(refresh.access_token)}

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)


class AuthSignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, min_length=1)
    email = serializers.EmailField(required=True, max_length=254)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('"me" is forbidden username')
        return value

    def validate(self, attrs):
        return super().validate(attrs)

    def validate(self, data):
        data = super().validate(data)

        if not User.objects.filter(
            username=data['username'],
            email=data['email'],
        ).exists():

            if User.objects.filter(
                username=data['username']
            ).exists():
                raise serializers.ValidationError(
                    'A user with that username already exists.')

            if User.objects.filter(
                email=data['email']
            ).exists():
                raise serializers.ValidationError(
                    'A user with this email already exists.')
        return data
