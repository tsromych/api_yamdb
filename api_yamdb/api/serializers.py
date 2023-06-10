from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        exclude = ("id",)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        exclude = ("id",)


class GetTitleSerializer(serializers.ModelSerializer):
    """Сериализатор вывода произведений."""
    genre = GenreSerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(
        read_only=True,
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )

    #Пример реализации рейтинга
    def get_rating(self, obj):
        """Подсчет рейтинга произведения."""
        pass


class PostTitleSerializer(serializers.ModelSerializer):
    """Сериализатор создания произведений."""
    category = SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
    )
    genre = SlugRelatedField(
        slug_field="slug",
        queryset=Genre.objects.all(),
        many=True,
        required=True,
    )

    class Meta:
        model = Title
        fields = ("__all__",)

    def validate_year(self, title_year):
        year = timezone.now().year
        if title_year > year:
            raise serializers.ValidationError(
                "Указанный год больше текущего!"
            )
        return title_year
