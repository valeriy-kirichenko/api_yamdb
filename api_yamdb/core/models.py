from django.db import models


class CategoryGenreModel(models.Model):
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Уникальное название латиницей'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ReviewCommentModel(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:30]
