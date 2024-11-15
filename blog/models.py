from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Blog(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(max_length=2551)
    img = models.ImageField(upload_to='images/')
    coordinates1 = models.CharField(max_length=255)
    coordinates2 = models.CharField(max_length=255)

    def __str__(self):
        return self.category



# динамическое фото
# регистрация юзера через админку
# push github
# README.txt
