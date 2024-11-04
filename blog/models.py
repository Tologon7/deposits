from django.db import models


class Coordinates(models.Model):
    coordinate1 = models.CharField(max_length=255)
    coordinate2 = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.coordinate1}, {self.coordinate2}"


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title



class Blog(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2551)
    img = models.ImageField(upload_to='images/')
    coordinates = models.ForeignKey(Coordinates, on_delete=models.CASCADE)




# название месторождение
# Описание
# динамическое фото
# координаты 2 поля
# регистрация юзера через админку
# динамическая категория
# push github
# README.txt
