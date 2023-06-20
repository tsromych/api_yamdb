from django.db import models


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(
        max_length=256,
        db_index=True,
    )
    year = models.IntegerField(
        db_index=True,
    )
    description = models.TextField(
        blank=True,
    )
    genre = models.ManyToManyField(
        "Genre",
        through="TitleGenre",
    )
    category = models.ForeignKey(
        "Category",
        related_name="titles",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.slug


class TitleGenre(models.Model):
    """Промежуточная таблица для связи произведений и жанров."""
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.title}, {self.genre}'
