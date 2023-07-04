import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdmin
from .serializers import (ConformationCodeSerializer, RoleUserSerializer,
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
        permission_classes=(IsAuthenticated, ),
        serializer_class=RoleUserSerializer
    )
    def get_me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSignUpView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        serializer.save()
        user, created = User.objects.get_or_create(
            username=username, email=email)
        if not created:
            user.confirmation_code = uuid.uuid4()
            user.save(update_fields=['confirmation_code'])
        send_mail(
            f'Код подтверждения пользователя {username}',
            f'Ваш код: {user.confirmation_code}',
            settings.EMAIL_HOST,
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
        if serializer.data['confirmation_code'] != user.confirmation_code:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        token = AccessToken.for_user(user)
        user.is_active = True
        user.save()
        return Response(
            {'token': f'{token}'},
            status=status.HTTP_200_OK
        )
