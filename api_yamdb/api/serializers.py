from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre


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
        return result['rating']


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
    rating = serializers.IntegerField(
        read_only=True,
        default=None,
    )

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

    def validate_genre(self, genre):
        if genre == []:
            raise serializers.ValidationError(
                'Поле со списком жанров не может быть пустым'
            )
        return genre

    def create(self, validated_data):
        genre = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for item in genre:
            TitleGenre.objects.get_or_create(genre=item, title=title)
        return title

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        reviews = Review.objects.filter(title_id=instance.id)
        if reviews:
            repr['rating'] = reviews.aggregate(Avg('score'))
        repr['genre'] = []
        genres = GenreSerializer(instance.genre.all(), many=True).data
        for genre in genres:
            repr['genre'].append(genre)
        repr['category'] = {
            'name': instance.category.name,
            'slug': instance.category.slug
        }
        return repr


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        )
        read_only_fields = ('author',)

    def validate(self, data):
        if Review.objects.filter(
            author=self.context['request'].user,
            title_id=self.context['view'].kwargs.get('title_id')
        ).exists() and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Нельзя оставить несколько отзывов на одно произведение.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date'
        )
        model = Comment
        read_only_fields = ('author',)
