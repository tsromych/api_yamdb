import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdmin
from users.serializers import (ConformationCodeSerializer, RoleUserSerializer,
                               UserCreateSerializer, UserSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для отображения всех пользователей сайта."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=('get', 'patch',),
        detail=False,
        url_path='me',
        permission_classes=([IsAuthenticated, ]),
        serializer_class=RoleUserSerializer
    )
    def get_me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        try:
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            raise error


def get_and_send_confirmation_code(user):
    user.update(confirmation_code=str(uuid.uuid4()))
    send_mail(
        'Код подтверждения',
        (f'Код подтверждения для пользователя "{user.username}":'
         f' {user.confirmation_code}'),
        settings.EMAIL_HOST_USER,
        [user.email]
    )


class UserSignUpView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username',)
        email = request.data.get('email',)
        try:
            user = User.objects.get(username=username, email=email)
            user.confirmation_code = uuid.uuid4()
            user.save(update_fields=['confirmation_code'])
        except User.DoesNotExist:
            serializer = UserCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user = get_object_or_404(User, username=username, email=email)
        send_mail(
            f'Код подтверждения пользователя {username}',
            f'Ваш код: {user.confirmation_code}',
            settings.EMAIL_HOST_USER,
            [f'{email}'],
            fail_silently=False
        )
        return Response(
            {'email': email, 'username': username},
            status=status.HTTP_200_OK
        )


class ConfirmCodeView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ConformationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializer.data['username'])
        if serializer.data['confirmation_code'] == user.confirmation_code:
            token = AccessToken.for_user(user)
            user.is_active = True
            user.save()
            return Response(
                {'token': f'{token}'},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
