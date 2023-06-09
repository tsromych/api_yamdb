from rest_framework.serializers import (ModelSerializer, SerializerMethodField,
                                        SlugRelatedField)

from reviews.models import Comment, Review, Title


class TitleSerializer(ModelSerializer):
    rating = SerializerMethodField()

    def get_rating(self, instance):
        return instance.average_rating()  # Вычисление среднего рейтинга

    class Meta:
        model = Title
        fields = ['rating']


class ReviewSerializer(ModelSerializer):
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


class CommentSerializer(ModelSerializer):
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
