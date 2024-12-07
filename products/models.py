from django.db import models
from django.urls import reverse


class Category(models.Model):                       # КАТЕГОРИИ ТОВАРОВ (ОДЕЖДА, ОБУВЬ, АКСЕССУАРЫ)
    name_category = models.CharField(max_length=50)

    """" Можно использовать в меню построение ссылки через МЕТОД get_absolute_url. 
    Смотри шаблон products/all_products.html
    Либо использовать ТЕГ {% url 'products-by-category' cat.id %}, 
    я предпочитаю создавать МЕТОДЫ в МОДЕЛИ и использовать их вместо {% url %}. """
    # МЕТОД через get_absolute_url:
    # def get_absolute_url(self):
    #     return reverse('products-by-category', kwargs={'category_id': self.id})


class Season(models.Model):
    name_season = models.CharField(max_length=50)


class Product(models.Model):
    name_product = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    image = models.ImageField('/product_image/')
    is_deleted = models.BooleanField(default=False)
    price = models.FloatField()

    # P.S. В принципе можно поле 'image' здесь НЕ прописывать,
    # а ВСЕ фотографии будут привязываться в class ProductImage(models.Model) через ForeignKey!

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name_product, self.price


class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField('/product_image/')
