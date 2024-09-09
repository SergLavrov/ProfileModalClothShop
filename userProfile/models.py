from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    phone = models.CharField(max_length=20, unique=True)
    postcode = models.CharField(max_length=6)
    about = models.TextField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)



# null=True - допустимое значение NULL в базе данных для поля !
# blank=True - поле может быть пустым !
# unique=True - поле должно быть уникальным !