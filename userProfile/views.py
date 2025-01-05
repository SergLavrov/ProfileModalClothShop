from django.contrib import messages
from django.shortcuts import render, redirect

from django.contrib.auth.models import User, Group
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .forms import ProfileForm
from .forms import RegistrationForm
from .models import Profile

from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, 'userProfile/home.html')


# <!-- 1 Вариант через class RegistrationForm(forms.Form): -->
def registration_form(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            # Обработка данных формы
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Сохранение данных в базу
            user = User.objects.create_user(username, email, password)
            user.save()

            messages.success(request, 'Вы успешно зарегистрированы!')

            return HttpResponseRedirect(reverse('home'))

        else:
            # return HttpResponseRedirect(reverse('home'))
            form.add_error(None, 'Не удалось создать пользователя')
    else:
        form = RegistrationForm()

    return render(request, 'userProfile/register_form.html', {'form': form})


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

    # ОСНОВНОЙ РАБОЧИЙ:
    # 1.0 Вариант Профиль пользователя просто через ШАБЛОН !add_profile2.html! через Models.py

# def add_profile_user(request):
#     if request.method == 'POST':  # Получение заполненой формы
#         user = request.user
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         age = request.POST.get('age')
#         phone = request.POST.get('phone')
#         postcode = request.POST.get('postcode')
#         about = request.POST.get('about')
#         time_created = request.POST.get('time_created')
#         image = request.FILES.get('image')         # ВАЖНО: ПОЛЕ image - FILE ! (request.FILES) !!!
#
#         try:
#             profile = Profile.objects.create(
#                 user=user,
#                 first_name=first_name,
#                 last_name=last_name,
#                 age=age,
#                 phone=phone,
#                 postcode=postcode,
#                 about=about,
#                 time_created=time_created,
#                 image=image,
#                 )
#
#             profile.save()
#
#             messages.success(request, 'Вы успешно создали профиль пользователя')
#             # return HttpResponseRedirect(reverse('profile_user'))
#             return HttpResponseRedirect(reverse('home'))
#
#         except:
#             messages.error(request, 'Не удалось создать профиль пользователя')
#             return HttpResponseRedirect(reverse('add-profile'))
#     else:
#         return render(request, 'userProfile/add_profile2.html')


    # 1.1 Вариант Профиль пользователя через ШАБЛОН

    #   Поскольку в шаблоне форма по умолчанию будет отправляться на тот же адрес, то представление обрабатывает сразу
#       два типа запросов GET и POST. Для определения типа запроса проверяем значение "request.method".
    #   Если запрос типа POST, то через объект "request.POST" получаем отправленные данные формы. Мы можем получить
    #   эти данные по отдельности для каждого поля формы. После этого отправляем пользователю сообещние - В принципе
    #   тут можно было бы сделать переадресацию или использовать другой шаблон для генерации ответа.
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
#             image = request.FILES.get('image')
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
#                 image=image,
#                 user=user)
#
#             profile.save()
#
#             return HttpResponseRedirect(reverse('home'))
#
#         except:
#             return HttpResponseRedirect(reverse('add-profile'))
#             # Для обработки всех возможных ошибок - например № телефона д.б. уникальным (см. Models.py)
#             # Тогда данные не отправляются, а перенаправляются на страницу профиля.
#
#     else:
#         return render(request, 'userProfile/add_profile_user.html', data)


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


# 1.3  Вариант - ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ через FORMS.py - через ШАБЛОН 'userProfile/profile_user.html'
#
# Подробнее про валидацию форм на METANIT- https://metanit.com/python/django/4.4.php

def add_profile_user(request):
    if request.method == 'POST':
        user = request.user
        form = ProfileForm(request.POST, request.FILES)  # ВАЖНО! для работы с файлами (дописать: request.FILES) !!!
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                age = form.cleaned_data.get('age')
                phone = form.cleaned_data.get('phone')
                postcode = form.cleaned_data.get('postcode')
                about = form.cleaned_data.get('about')
                image = form.cleaned_data.get('image')
                user = user

                profile = Profile.objects.create(first_name=first_name,
                                                 last_name=last_name,
                                                 age=age,
                                                 phone=phone,
                                                 postcode=postcode,
                                                 about=about,
                                                 image=image,
                                                 user=user)
                profile.save()

                return HttpResponseRedirect(reverse('home'))

        except:
            form.add_error(None, 'Не удалось создать профиль пользователя')
            # Для обработки всех возможных ошибок - например № телефона д.б. уникальным (см. Models.py)
            # return HttpResponse("Invalid data")
    else:
        form = ProfileForm()

    data = {
        'form': form
    }

    return render(request, 'userProfile/add_profile_user.html', data)


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
#             profile.image = form.cleaned_data['image']
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


# Если хотим вывести список ВСЕХ профилей !
def profile_users_list(request):
    if request.user.is_staff:
        profiles = Profile.objects.all()

        data = {
            'profiles': profiles
        }
        return render(request, 'userProfile/profile_list.html', data)

    else:
        messages.error(request, 'У Вас нет прав администратора!')
        return redirect(reverse('home'))


def profile_user(request):
    if Profile.objects.filter(user=request.user).exists():
        profile = Profile.objects.get(user=request.user)

        return render(request, 'userProfile/my_profile.html', {'profile': profile})
    else:
        messages.error(request, 'Создайте профиль!')

        return HttpResponseRedirect(reverse('add-profile'))
        # return HttpResponseRedirect(reverse('home'))


def delete_profile_user(request):
    if request.user.is_authenticated:
        prof = Profile.objects.get(user=request.user)
        prof.delete()
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('home'))


# def delete_ticket(request, ticket_id: int):
#     ticket = Ticket.objects.get(id=ticket_id)
#     ticket.delete()
#     return redirect('ticket-list')


# Просто пример!

# def get_products_list(request: HttpRequest) -> HttpResponse:
#     if request.user.is_authenticated:
#         user = request.user
#         products = Product.objects.filter(company__name_company=user)
#
#         return render(request, 'products/products_list.html', {'products': products})
#     else:
#         return render(request, 'userAdmin/login.html')
