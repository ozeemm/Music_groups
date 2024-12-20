# Generated by Django 5.1.1 on 2024-10-22 04:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_groups', '0002_genre_remove_group_genre_album_genre'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'verbose_name': 'Участник группы', 'verbose_name_plural': 'Участнки групп'},
        ),
        migrations.AddField(
            model_name='album',
            name='image',
            field=models.ImageField(null=True, upload_to='music_groups', verbose_name='Обложка'),
        ),
        migrations.AlterField(
            model_name='album',
            name='genre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='music_groups.genre', verbose_name='Жанр'),
        ),
        migrations.AlterField(
            model_name='album',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='music_groups.group', verbose_name='Группа'),
        ),
        migrations.AlterField(
            model_name='member',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='music_groups.group', verbose_name='Группа'),
        ),
        migrations.AlterField(
            model_name='song',
            name='album',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='music_groups.album', verbose_name='Альбом'),
        ),
    ]
