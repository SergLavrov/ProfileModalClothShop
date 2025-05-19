from django.db import models
from django.urls import reverse


class Category(models.Model):                       # КАТЕГОРИИ ТОВАРОВ (ОДЕЖДА, ОБУВЬ, АКСЕССУАРЫ)
    name_category = models.CharField(max_length=50)

    """" Можно использовать в меню построение ссылки через МЕТОД get_absolute_url. 
    Смотри шаблон products/all_products.html
    Либо использовать ТЕГ {% url 'products-by-category' cat.id %}, 
    я предпочитаю создавать МЕТОДЫ в МОДЕЛИ и использовать их вместо {% url %}. """
    # ЭТО МЕТОД через get_absolute_url():
    # def get_absolute_url(self):
    #     return reverse('products-by-category', kwargs={'category_id': self.id})


class Season(models.Model):
    name_season = models.CharField(max_length=50)


class Size(models.Model):
    name_size = models.IntegerField(max_length=56)

# null=True - допустимое значение NULL в базе данных для поля !
# blank=True - поле может быть пустым !
# unique=True - поле должно быть уникальным !
"""
Many To Many !!! - ХОРОШИЙ ПРИМЕР !!!! С ПОЯСНЕНИЕМ см на сайте METANIT:
https://metanit.com/python/django/5.11.php
https://metanit.com/python/django/5.7.php
"""


class Product(models.Model):
    # sizes = models.ManyToManyField(Size, through='ProductInfo')
    sizes = models.ManyToManyField(Size, related_name='products_sizes')
    name_product = models.CharField(max_length=50)
    article = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    image = models.ImageField('/product_image/')
    is_deleted = models.BooleanField(default=False)
    price = models.FloatField()
    quantity = models.PositiveIntegerField(default=0)


# class ProductInfo(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     size = models.ForeignKey(Size, on_delete=models.CASCADE)
#     prod_count = models.PositiveIntegerField(default=0)
#     price_size = models.FloatField(default=0)
#     date_add = models.DateTimeField(auto_now_add=True)

    """
    Пояснение для поля 'quantity':
    Установка значений по умолчанию делает ввод данных более понятным. Используем параметр default=0 для задания 
    начального значения поля! Таким образом, quantity будет начинаться с "нуля".
    Справочник типов полей:
    https://django.fun/docs/django/5.0/ref/models/fields/    
    PositiveIntegerField - (положительное целое число) должно быть либо положительным, либо нулевым (0). 
    Значения от 0 до 2147483647 безопасны во всех БД, поддерживаемых Django. 
    Значение 0 принимается по причинам обратной совместимости.
    """
    # P.S. В принципе можно поле 'image' здесь НЕ прописывать,
    # а ВСЕ фотографии будут привязываться в class ProductImage(models.Model) через ForeignKey!

    class Meta:
        ordering = ['id']

    # def __str__(self):
    #     return self.name_product, self.price


class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField('/product_image/')



