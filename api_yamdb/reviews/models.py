from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (CASCADE, SET_NULL, Avg, CharField, DateTimeField,
                              ForeignKey, IntegerField, Model,
                              PositiveIntegerField, TextField, UniqueConstraint)

from django.utils.timezone import now

User = get_user_model()


class Genre(Model):
    name = CharField(max_length=255)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(Model):
    name = CharField(max_length=255)

    def average_rating(self):
        return (self.reviews.aggregate(avg_rating=Avg('rating'))
                .get('avg_rating'))

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Category(Model):
    name = CharField(max_length=255)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Review(Model):
    title = ForeignKey(
        Title,
        on_delete=CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    text = CharField(max_length=200)
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    rating = IntegerField(
        'оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={
            'validators': 'Пожалуйста, поставьте оценку от 1 до 10'
        }
    )
    pub_date = DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            UniqueConstraint(
                fields=('title', 'author', ),
                name='unique review'
            )]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comment(Model):
    review = ForeignKey(
        Review,
        on_delete=CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )
    text = CharField('текст комментария', max_length=200)
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='comments',
        verbose_name='автор'
    )
    pub_date = DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
