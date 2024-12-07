from django.shortcuts import render, get_object_or_404
from products.models import Product, Category, Season, ProductImage
from django.http import HttpResponseRedirect
from django.urls import reverse
# from django.contrib.auth.models import User


def get_products_list(request):
    """ Вывод списка товаров в виде таблицы для авторизованных пользователей """
    user = request.user
    if user.is_authenticated:
        products = Product.objects.all()

        data = {
            'products': products
        }
        return render(request, 'products/products_list.html', data)


# def get_products(request):
#     user = request.user
#     categories = Category.objects.all()
#     if user.is_authenticated:
#         products = Product.objects.all()
#         data = {
#             'products': products
#         }
#         return render(request, 'products/products_list.html', data)
#
#     else:
#         products = Product.objects.filter(is_deleted=False)
#         data = {
#             'products': products,
#             'categories': categories
#         }
#         return render(request, 'products/all_products.html', data)


# 0. Вариант Фильтр товаров по категориям ! РАБОЧИЙ ВАРИАНТ !!!
# def get_products(request, category_id=None):
#     """" К продукту мы можем обращаться с помощью вспомогательной функции Django get_object_or_404.
#     Эта функция получает запрошенный объект из базы данных, а в случае его отсутствия инициирует исключение 404. """
#     category = None
#     categories = Category.objects.all()
#     products = Product.objects.filter(is_deleted=False)
#
#     if category_id:
#         category = get_object_or_404(Category, id=category_id)
#         # category = Category.objects.get(id=category_id)
#         products = products.filter(category=category)
#
#     if not products:
#         return render(request, 'products/nothing_is_find.html')
#
#     data = {
#         'category': category,
#         'categories': categories,
#         'products': products
#     }
#     return render(request, 'products/all_products.html', data)


# 1. Вариант Фильтр по категориям, если делать ссылку на категорию - НЕ через CHECKBOX. РАБОЧИЙ ВАРИАНТ !!!
# def get_products(request, category_id=None):
#     category_list = Category.objects.all()
#
#     if category_id:
#         category = Category.objects.get(id=category_id)
#         products = Product.objects.filter(category=category).filter(is_deleted=False)
#
#     else:
#         products = Product.objects.filter(is_deleted=False)
#
#     data = {
#         'categories': category_list,
#         'products': products,
#     }
#     return render(request, 'products/all_products.html', data)


# 1.1 Вариант Фильтр по сезонам, если делать ЧЕРЕЗ ССЫЛКУ на сезон - НЕ через CHECKBOX. РАБОЧИЙ ВАРИАНТ !!!
def get_products(request, season_id=None):
    season_list = Season.objects.all()
    category_list = Category.objects.all() # Для бокового фильтра через checkbox!

    if season_id:
        season = Season.objects.get(id=season_id)
        products = Product.objects.filter(season=season).filter(is_deleted=False)

        if not products:
            return render(request, 'products/nothing_is_find.html')

    else:
        products = Product.objects.filter(is_deleted=False)

    data = {
        'categories': category_list, # Для бокового фильтра через checkbox!
        'seasons': season_list,
        'products': products,
    }
    return render(request, 'products/all_products.html', data)


def get_sorted_products(request):
    if request.method == 'POST':
        season_list = Season.objects.all()
        category_list = Category.objects.all() # Для бокового фильтра через checkbox!

        products_list = Product.objects.filter(is_deleted=False)

        sorted_value = request.POST.get('select_value')
        # 'select_value' - это name - берем из шаблона - <select name="select_value" class="form-select">
        # Используем get (а не getlist) т.к. нам нужно получить только ОДНО нужное значение value !!!
        # В функцию передается выбранное значение value1 или value2 или value3 или value4 из выпадающего списка.
        # Сортируем по нужному значению: price, name_product или -price, -name_product

        if sorted_value == 'value1':
            products_list = products_list.filter(is_deleted=False).order_by('price')
        if sorted_value == 'value2':
            products_list = products_list.filter(is_deleted=False).order_by('-price')
        if sorted_value == 'value3':
            products_list = products_list.filter(is_deleted=False).order_by('name_product')
        if sorted_value == 'value4':
            products_list = products_list.filter(is_deleted=False).order_by('-name_product')

        data = {
            'categories': category_list,
            'seasons': season_list,
            'products': products_list,
        }
        return render(request, 'products/all_products.html', data)


def checkbox_products(request):
    if request.method == 'POST':
        """ Нужно использовать getlist для получения всех выбранных значений из нашего чекбокса, 
            иначе при использовании get будет возвращено только последнее выбранное значение. """

        season_list = Season.objects.all()
        category_list = Category.objects.all()

        id_categories_list = request.POST.getlist('categories')     # getlist
        # name_categories_list = request.POST.getlist('categories')

        id_seasons_list = request.POST.getlist('seasons')       # getlist
        # name_seasons_list = request.POST.getlist('seasons')      # ('seasons') из шаблона all_products.html
                                                                   # < input type = "checkbox" name="seasons">
        name_products_list = request.POST.getlist('prod_names') # getlist

        products_list = Product.objects.all().filter(is_deleted=False)

        # 1 Вариант через "name_categories_list"
        # if name_categories_list:
        #     products_list = products_list.filter(category__name_category__in=name_categories_list).filter(is_deleted=False)

        # 2 Вариант через "id_categories_list"
        if id_categories_list:
            products_list = products_list.filter(category__id__in=id_categories_list).filter(is_deleted=False)

        # 1 Вариант через "name_seasons_list"
        # if name_seasons_list:
        #     products_list = products_list.filter(season__name_season__in=name_seasons_list).filter(is_deleted=False)

        # 2 Вариант через "id_seasons_list"
        if id_seasons_list:
            products_list = products_list.filter(season__id__in=id_seasons_list).filter(is_deleted=False)

        if name_products_list:
            products_list = products_list.filter(name_product__in=name_products_list).filter(is_deleted=False)

        if not products_list:
            return render(request, 'products/nothing_is_find.html')

        data = {
            'products': products_list,
            'seasons': season_list,
            'categories': category_list,
        }
        return render(request, 'products/all_products.html', data)

    # else:
    #     products_list = Product.objects.all().filter(is_deleted=False)
    #     season_list = Season.objects.all()
    #     category_list = Category.objects.all()
    #
    #     data = {
    #         'products': products_list,
    #         'seasons': season_list,
    #         'categories': category_list,
    #     }
    #     return render(request, 'products/all_products.html', data)


# # 2. Вариант Фильтр по категориям ! РАБОЧИЙ ВАРИАНТ !!!
# """" Обновляем ШАБЛОН.html в зависимости от того, нужно сделать ФИЛЬТР по category_id или нет"""
# def get_products(request, category_id=None):
#     category_list = Category.objects.all()
#     data = {
#         'categories': category_list
#     }
#     if category_id:
#         data.update({'products': Product.objects.filter(category__id=category_id).filter(is_deleted=False)})
#     else:
#         data.update({'products': Product.objects.filter(is_deleted=False)})
#
#     return render(request, 'products/all_products.html', data)


def get_products_by_filter(request, config: str, value: str):
    # products = Product.objects.filter(**{config: value})
    # category_list = Category.objects.all()
    # season_list = Season.objects.all()
    # config = ['category', 'season', 'name_product', 'color'][int(config) - 1]

    if config == 'category':
        products = Product.objects.filter(category__name_category=value).filter(is_deleted=False)
    elif config == 'season':
        products = Product.objects.filter(season__name_season=value).filter(is_deleted=False)
    elif config == 'name_product':
        products = Product.objects.filter(name_product=value).filter(is_deleted=False)
    elif config == 'color':
        products = Product.objects.filter(color=value).filter(is_deleted=False)
    else:
        products = Product.objects.filter(is_deleted=False)

    data = {
        # 'categories': category_list,
        # 'seasons': season_list,
        'products': products,
        # dict: {'config': config, 'value': value},
        # 'config': config,
        # 'value': value
    }
    return render(request, 'products/filter_type_value.html', data)


def add_product(request):
    if request.method == 'POST':
        name_product = request.POST.get('name_product')
        color = request.POST.get('color')
        category_id = request.POST.get('category_id')
        season_id = request.POST.get('season_id')
        image = request.FILES.get('image')
        # is_deleted = request.POST.get('is_deleted')

        category = Category.objects.get(id=category_id)
        season = Season.objects.get(id=season_id)

        product = Product.objects.create(
            name_product=name_product,
            color=color,
            category=category,
            season=season,
            image=image,
        )
        product.save()

        images = request.FILES.getlist('images_for_getlist')

        for image in images:
            # img = ProductImage(product=product, image=image)
            img = ProductImage.objects.create(
                product=product,
                image=image,
            )
            img.save()

        return HttpResponseRedirect(reverse('get-products-list'))

    else:
        category_list = Category.objects.all()
        season_list = Season.objects.all()
        data = {
            'categories': category_list,
            'seasons': season_list,
        }

        return render(request, 'products/add_product.html', data)


def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    images = ProductImage.objects.filter(product=product)

    data = {
        'product': product,
        'images': images,
    }
    return render(request, 'products/product_detail.html', data)


def delete_product(request, product_id):
    product = Product.objects.get(id=product_id, name=id)
    product.is_deleted = True
    product.save()
    return HttpResponseRedirect(reverse('get-products-list'))
