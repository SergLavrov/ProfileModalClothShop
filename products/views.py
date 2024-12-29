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


# 1. Вариант Фильтр по категориям, если делать ССЫЛКУ на категорию - НЕ через CHECKBOX. РАБОЧИЙ ВАРИАНТ !!!
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
    name_list = Product.objects.values('name_product').order_by('name_product').distinct('name_product')
                                           # Для def get_config - см. ниже!

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
        'name_list': name_list # Для выпадающего списка - "СПИСОК ТОВАРОВ":
    }
    return render(request, 'products/all_products.html', data)


def get_typ_value_dropdown(request, typ, value):
    """ Выпадающий список через ССЫЛКУ ! (НЕ через SELECT / <option>) """
    season_list = Season.objects.all()
    category_list = Category.objects.all()  # Для бокового фильтра через checkbox!
    name_list = Product.objects.values('name_product').order_by('name_product').distinct('name_product')

    if typ == 'category':
        products_list = Product.objects.filter(category__name_category=value).filter(is_deleted=False)
    elif typ == 'season':
        products_list = Product.objects.filter(season__name_season=value).filter(is_deleted=False)
    elif typ == 'name_product':
        products_list = Product.objects.filter(name_product=value).filter(is_deleted=False)
    elif typ == 'color':
        products_list = Product.objects.filter(color=value).filter(is_deleted=False)
    else:
        products_list = Product.objects.filter(is_deleted=False)

    if not products_list:
        return render(request, 'products/nothing_is_find.html')

    data = {
        'products': products_list,
        'categories': category_list,
        'seasons': season_list,
        'name_list': name_list
    }
    return render(request, 'products/all_products.html', data)


# def get_value_dropdown(request, value):
#     """ Выпадающий список через ССЫЛКУ ! (НЕ через SELECT / <option>) """
#     season_list = Season.objects.all()
#     category_list = Category.objects.all()  # Для бокового фильтра через checkbox!
#     name_list = Product.objects.values('name_product').order_by('name_product').distinct('name_product')
#                                                                         # Для def get_config - см. ниже!
#     products_list = Product.objects.filter(is_deleted=False)
#     if (value == 'Брюки' or value == 'Джемпер' or value == 'Джинсы' or value == 'Пальто' or value == 'Ботинки' or
#             value == 'Туфли' or value == 'Кроссовки' or value == 'Галстук' or value == 'Ремень'):
#         products_list = products_list.filter(name_product=value).filter(is_deleted=False)
#
#         data = {
#             'products': products_list,
#             'categories': category_list,  # Для бокового фильтра через checkbox!
#             'seasons': season_list,
#             'name_list': name_list        # Для выпадающего списка - "СПИСОК ТОВАРОВ":
#         }
#         return render(request, 'products/all_products.html', data)


#   1 ВАРИАНТ: через "name_category"
# def get_value_dropdown_category(request, value):
#     """ Выпадающий список "КАТЕГОРИИ" через ССЫЛКУ ! (НЕ через SELECT / <option>) """
#     season_list = Season.objects.all()
#     category_list = Category.objects.all()  # Для бокового фильтра через checkbox!
#     name_list = Product.objects.values('name_product').order_by('name_product').distinct('name_product')
#                                                                         # Для def get_config - см. ниже!
#     products_list = Product.objects.filter(category__name_category=value).filter(is_deleted=False)
#
#     data = {
#         'products': products_list,
#         'categories': category_list,  # Для бокового фильтра через checkbox!
#         'seasons': season_list,
#         'name_list': name_list  # Для выпадающего списка - "СПИСОК ТОВАРОВ":
#     }
#     return render(request, 'products/all_products.html', data)


#     2 ВАРИАНТ: через id категории
# def get_value_dropdown_category(request, value):
#     """ Выпадающий список "КАТЕГОРИИ" через ССЫЛКУ ! (НЕ через SELECT / <option>) """
#     season_list = Season.objects.all()
#     category_list = Category.objects.all()  # Для бокового фильтра через checkbox!
#     name_list = Product.objects.values('name_product').order_by('name_product').distinct('name_product')
#                                                                         # Для def get_config - см. ниже!
#     products_list = Product.objects.filter(is_deleted=False)
#     category = Category.objects.get(id=value)
#     if category:
#         products_list = products_list.filter(category__id=value).filter(is_deleted=False)
#
#         data = {
#             'products': products_list,
#             'categories': category_list,  # Для бокового фильтра через checkbox!
#             'seasons': season_list,
#             'name_list': name_list  # Для выпадающего списка - "СПИСОК ТОВАРОВ":
#         }
#         return render(request, 'products/all_products.html', data)


    # P.S. Для выпадающего списка - "СПИСОК ТОВАРОВ":
    # Используем МЕТОДЫ: .values() и .order_by() и .distinct() !!! см. ниже !!!
    # Получаем список уникальных названий продуктов (т.е.продукты в выпадающем списке будут без повторов!!!):

    # МЕТОД distinct() возвращает новый QuerySet, который использует SELECT DISTINCT в своем SQL - запросе.
    # Это исключает повторяющиеся строки из рез-тов запроса. По умолчанию QuerySet не удаляет повторяющиеся строки.

    # МЕТОД values() возвращает словари ! Мы можем извлекать только те поля, которые нам требуются,
    # передавая их имена в качестве аргументов!
    # < QuerySet[{'name_product': 'Ботинки'}, {'name_product': 'Брюки'}, {'name_product': 'Галстук'},
    # {'name_product': 'Джемпер'}, {'name_product': 'Джинсы'}, {'name_product': 'Кроссовки'},
    # {'name_product': 'Пальто'}, {'name_product': 'Ремень'}, {'name_product': 'Туфли'}] >


# def get_config_value_products(request, config=None, value=None):
def get_config(request):
    if request.method == 'POST':
        category_list = Category.objects.all()
        season_list = Season.objects.all()
        products_list = Product.objects.filter(is_deleted=False)

        # Для выпадающего списка - "СПИСОК ТОВАРОВ":
        name_list = products_list.values('name_product').order_by('name_product').distinct('name_product')
        # для использования в шаблоне --> см. {% for p in name_list %}
        # print(name_list)  # Чтобы посмотреть что получилось!

        # Пробовал:
        # name_list = Product.objects.values_list('name_product', flat=True).distinct()
        # name_list = Product.objects.order_by('name_product').distinct('name_product')

        # name_list = []
        # for name in name_list:
        #     if name not in name_list:
        #         name_list.append(name)

        category_id = request.POST.get('category_id')  # берем из шаблона из: name="category_id"!

        name_select = request.POST.get('name_prod')  # получаем одно нужное значение из шаблона - name="name_prod"!

        cloth_name_value = request.POST.get('name_cloth') # берем одно значение из шаблона из: name="name_cloth"!
        # print(cloth_name_value) # Чтобы посмотреть какое value выбралось: "Брюки", "Джемпер", "Джинсы", "Пальто" !!!

        if category_id:
            category = Category.objects.get(id=category_id)
            products_list = products_list.filter(category=category).filter(is_deleted=False)

        elif name_select:
            products_list = products_list.filter(name_product=name_select).filter(is_deleted=False)

        elif cloth_name_value:
            products_list = products_list.filter(name_product=cloth_name_value).filter(is_deleted=False)

        else:
            products_list = Product.objects.filter(is_deleted=False)

        data = {
            'categories': category_list,
            'seasons': season_list,
            'products': products_list,
            'name_list': name_list,
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

        # 1. Вариант через "name_categories_list"
        # if name_categories_list:
        #     products_list = products_list.filter(category__name_category__in=name_categories_list).filter(is_deleted=False)

        # 1.1 Вариант через "id_categories_list"
        if id_categories_list:
            products_list = products_list.filter(category__id__in=id_categories_list).filter(is_deleted=False)

        # 2. Вариант через "name_seasons_list"
        # if name_seasons_list:
        #     products_list = products_list.filter(season__name_season__in=name_seasons_list).filter(is_deleted=False)

        # 2.1 Вариант через "id_seasons_list"
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


def add_product(request):
    if request.method == 'POST':
        name_product = request.POST.get('name_product') # name="name_product" из шаблона add_product.html
        color = request.POST.get('color')               # name="color" из шаблона add_product.html
        category_id = request.POST.get('category_id')   # name="category_id" из шаблона add_product.html
        season_id = request.POST.get('season_id')       # name="season_id" из шаблона add_product.html
        image = request.FILES.get('image')              # name="image" из шаблона add_product.html
        # is_deleted = request.POST.get('is_deleted')#

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

        images = request.FILES.getlist('images_for_getlist') # name="images_for_getlist" из шаблона add_product.html

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
    product = Product.objects.get(id=product_id)
    product.is_deleted = True
    product.save()
    return HttpResponseRedirect(reverse('get-products-list'))
