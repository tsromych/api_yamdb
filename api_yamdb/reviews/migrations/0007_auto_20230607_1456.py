# Generated by Django 3.2 on 2023-06-07 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_auto_20230607_1448'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.RemoveField(
            model_name='comment',
            name='created',
        ),
        migrations.AddField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=1, verbose_name='дата публикации'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.CharField(max_length=200, verbose_name='текст комментария'),
        ),
    ]