from django.db.models import Avg
from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


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
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def get_rating(self, obj):
        """Подсчет рейтинга произведения."""
        if obj.reviews.count() == 0:
            return None
        result = Review.objects.filter(title=obj).aggregate(
            rating=Avg('score'))
        return result['raring']


class PostTitleSerializer(serializers.ModelSerializer):
    """Сериализатор создания произведений."""
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=True,
    )
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )

    def validate_year(self, title_year):
        year = timezone.now().year
        if title_year > year:
            raise serializers.ValidationError(
                'Указанный год больше текущего!'
            )
        return title_year


class ReviewSerializer(serializers.ModelSerializer):
    title = SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    review = SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
