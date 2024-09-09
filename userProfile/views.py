from django.shortcuts import render

from django.contrib.auth.models import User, Group
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .forms import ProfileForm
from .models import Profile

from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, 'userProfile/home.html')


# <!-- 1 Вариант через MODAL window for REGISTRATION -->

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists(): # проверка на существование пользователя по имени #
            return HttpResponseRedirect(reverse('home')) # ИНАЧЕ перенаправляем на страницу с продуктами!

        if User.objects.filter(email=email).exists(): # проверка на существование пользователя по email #
            return HttpResponseRedirect(reverse('home'))

        if not username or not email or not password or not confirm_password: # Проверка, чтобы не было пустых полей!
            return HttpResponseRedirect(reverse('home'))  # Иначе перенаправляем на страницу с продуктами

        if password != confirm_password:
            return HttpResponseRedirect(reverse('home'))

        # group_user = Group.objects.get(name='users')

        user = User.objects.create_user(username, email, password)
        # user.groups.add(group_user)
        user.save()
        # login(request, user) # (Вместо - user.save()) Так можно сделать, если хотим сразу после регистрации "ВОЙТИ НА САЙТ!"

        return HttpResponseRedirect(reverse('home'))
        # return HttpResponseRedirect(reverse('login_user'))
    else:
        return HttpResponseRedirect(reverse('home'))


    # 1.1 Вариант Профиль пользователя через ШАБЛОН

    #   Поскольку в шаблоне форма по умолчанию будет отправляться на тот же адрес, то представление обрабатывает сразу
    # два типа запросов GET и POST. Для определения типа запроса проверяем значение "request.method".
    #   Если запрос типа POST, то через объект "request.POST" получаем отправленные данные формы. Мы можем получить
    # эти данные по отдельности для каждого поля формы. После этого отправляем пользователю сообещние - В принципе
    # тут можно было бы сделать переадресацию или использовать другой шаблон для генерации ответа.
    #   Если запрос представляет тип GET, то создаем объект UserForm - выводим форму для ввода данных и отправляем ее
    #   в составе веб - страницы home.html. Таким образом, при обращении к приложению мы вначале  увидим ФОРМУ ВВОДА.
    #   Введем в нее некоторые данные:

# def add_profile_user(request):
#     if request.method == 'POST':                       # Получение заполненой формы
#         try:
#             first_name = request.POST.get('first_name')
#             last_name = request.POST.get('last_name')
#             age = request.POST.get('age')
#             phone = request.POST.get('phone')
#             postcode = request.POST.get('postcode')
#             about = request.POST.get('about')
#             time_created = request.POST.get('time_created')
#             user = request.user
#
#             profile = Profile.objects.create(
#                 first_name=first_name,
#                 last_name=last_name,
#                 age=age,
#                 phone=phone,
#                 postcode=postcode,
#                 about=about,
#                 time_created=time_created,
#                 user=user)
#
#             profile.save()
#
#             return HttpResponseRedirect(reverse('home'))
#
#         except:
#             return HttpResponseRedirect(reverse('profile'))
#             # Для обработки всех возможных ошибок - например № телефона д.б. уникальным (см. Models.py)
#             # Тогда данные не отправляются, а перенаправляются на страницу профиля.
#
#     else:
#         form = ProfileForm()   # Получение пустой ФОРМЫ ВВОДА
#
#         data = {
#             'form': form
#         }
#         return render(request, 'userProfile/profile_user.html', data)


# 1.2 Вариант через ШАБЛОН
# Подробнее про валидацию форм на METANIT- https://metanit.com/python/django/4.4.php

# def add_profile_user(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST)
#         if form.is_valid():
#             try:
#                 Profile.objects.create(**form.cleaned_data)
#                 return HttpResponseRedirect(reverse('home'))
#
#             except:
#                 form.add_error(None, 'Не удалось создать профиль пользователя')
#     else:
#         form = ProfileForm()
#
#     data = {
#         'form': form
#     }
#     return render(request, 'userProfile/profile_user.html', data)


# 1.3  Вариант - ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ через ШАБЛОН 'userProfile/profile_user.html'
#
# Подробнее про валидацию форм на METANIT- https://metanit.com/python/django/4.4.php

def add_profile_user(request):
    """
    Если метод запроса POST, валидирует данные формы,
    создает новый объект профиля profile = Profile() и заполняет его данными формы,
    сохраняет его в базе данных и перенаправляет на страницу 'home' при успешном создании.
    В случае ошибок добавляется сообщение об ошибке к форме.
    """
    if request.method == 'POST':
        user = request.user
        form = ProfileForm(request.POST)

        if form.is_valid():
            try:
                profile = Profile()
                profile.first_name = form.cleaned_data['first_name']
                profile.last_name = form.cleaned_data['last_name']
                profile.age = form.cleaned_data['age']
                profile.phone = form.cleaned_data['phone']
                profile.postcode = form.cleaned_data['postcode']
                profile.about = form.cleaned_data['about']
                profile.user = user
                profile.save()

                return HttpResponseRedirect(reverse('home'))

            except:
                form.add_error(None, 'Не удалось создать профиль пользователя')
                # return HttpResponse("Invalid data")

        # else:
        #     return HttpResponseRedirect(reverse('home'))
    else:
        form = ProfileForm()

    data = {
        'form': form
    }

    return render(request, 'userProfile/profile_user.html', data)


# 2.  Вариант - ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ через МОДАЛЬНОЕ ОКНО data-target="#profileModal"
# def add_profile_user(request):
#
#     if request.method == 'POST':
#         user = request.user
#         form = ProfileForm(request.POST)
#
#         if form.is_valid():
#             profile = Profile()
#             profile.first_name = form.cleaned_data['first_name']
#             profile.last_name = form.cleaned_data['last_name']
#             profile.age = form.cleaned_data['age']
#             profile.phone = form.cleaned_data['phone']
#             profile.postcode = form.cleaned_data['postcode']
#             profile.about = form.cleaned_data['about']
#             profile.user = user
#             profile.save()
#
#             return HttpResponseRedirect(reverse('home'))
#
#         else:
#             form.add_error(None, 'Не удалось создать профиль пользователя')
#             # return HttpResponse("Invalid data")
#     else:
#         return HttpResponseRedirect(reverse('home'))


# <!-- через MODAL window for LOGIN -->

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
            # return HttpResponseRedirect(reverse('profile'))

        # < !-- если пользователь с таким именем/паролем НЕ существует -->
        return HttpResponseRedirect(reverse('home'))

    else:
        return HttpResponseRedirect(reverse('home'))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
