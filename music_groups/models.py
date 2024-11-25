from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.TextField("Название")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
    
    def __str__(self) -> str:
        return self.name

class Member(models.Model):
    name = models.TextField("Имя")
    group = models.ForeignKey("Group", verbose_name="Группа", on_delete=models.CASCADE, null=True)
    role = models.TextField("Роль в группе")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Участник группы"
        verbose_name_plural = "Участнки групп"

class MemberImage(models.Model):
    member = models.ForeignKey("Member", verbose_name="Участник", on_delete=models.CASCADE, null=True)
    image = models.ImageField("Фотография", null=True, blank=True, upload_to="music_groups/members")

    class Meta:
        verbose_name = "Фотография участника"
        verbose_name_plural = "Фотографии участников"

class Album(models.Model):
    name = models.TextField("Название")
    year = models.IntegerField("Год релиза")
    group = models.ForeignKey("Group", verbose_name="Группа", on_delete=models.CASCADE, null=True)
    genre = models.ForeignKey("Genre", verbose_name="Жанр", on_delete=models.CASCADE, null=True)
    image = models.ImageField("Обложка", null=True, blank=True, upload_to="music_groups/albums")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"
    
    def __str__(self) -> str:
        return self.name

class Song(models.Model):
    name = models.TextField("Название")
    album = models.ForeignKey("Album", verbose_name="Альбом", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Песня"
        verbose_name_plural = "Песни"

class Genre(models.Model):
    name = models.TextField("Название")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
    
    def __str__(self) -> str:
        return self.name