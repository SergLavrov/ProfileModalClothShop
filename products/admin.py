from django.contrib import admin
from .models import Product, Category, Season, ProductImage, Size

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Season)
admin.site.register(ProductImage)
admin.site.register(Size)
