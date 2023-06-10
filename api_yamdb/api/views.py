# from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
#from rest_framework.permissions import IsAuthenticated

from api.filters import TitleFilters
from api.mixins import TitlesViewSet
from api.permissions import AuthorPermission
from api.serializers import (CategorySerializer, GenreSerializer,
                             GetTitleSerializer, PostTitleSerializer)
from reviews.models import Category, Genre, Title


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет произведений."""
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilters

    def get_serializer_class(self):
        if self.request.method in ("POST", "PATCH"):
            return PostTitleSerializer
        return GetTitleSerializer


class GenreViewSet(TitlesViewSet):
    """Вьюсет жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorPermission,)
    filter_backends = (SearchFilter,)
    search_fields = "name"
    lookup_field = "slug"


class CategoryViewSet(TitlesViewSet):
    """Вьюсет категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorPermission,)
    filter_backends = (SearchFilter,)
    search_fields = "name"
    lookup_field = "slug"
