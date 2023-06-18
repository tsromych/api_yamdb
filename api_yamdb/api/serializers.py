from rest_framework.serializers import (ModelSerializer, SerializerMethodField,
                                        SlugRelatedField)

from reviews.models import Comment, Review, Title
from django.db.models import Avg


class TitleSerializer(ModelSerializer):
    score = SerializerMethodField()

    def get_score(self, instance):
        return instance.reviews.aggregate(
            avg_score=Avg('score')).get('avg_score')

    class Meta:
        model = Title
        fields = ['score']


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
