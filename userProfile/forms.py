from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible


# Вариант "РЕГИСТРАЦИИ" через forms.py (В models.py Класс для регистрации НЕ создается):
class RegistrationForm(forms.Form):
    username = forms.CharField(validators=[
                                   MinLengthValidator(3, message='Минимум 3 символа'),
                                   MaxLengthValidator(10, message='Максимум 10 символов'),
                               ])
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    # Валидация НА УРОВНЕ ФОРМЫ:
    # Помимо валидации отдельных полей, вы можете выполнять валидацию на уровне всей формы.
    # Это полезно, когда вам нужно проверить зависимость между несколькими полями или выполнить комплексные проверки.
    def clean_confirm_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают!")

    # ПОЛЬЗОВАТЕЛЬСКАЯ валидация:
    # Вы можете добавить собственные правила валидации, переопределив метод
    # clean в классе формы или создав методы clean_ < fieldname > для отдельных полей.
    def clean_username(self):
        username = self.cleaned_data['username']
        # if len(username) < 5:
        if ' ' in username:
            raise forms.ValidationError("Логин не должен содержать пробелов!")
        return username

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if len(username) < 3:
    #         raise forms.ValidationError("Логин слишком короткий!")
    #     return username

# ВСЕ поля-классы можно посмотреть в документации на django.forms - FORM fields

# Справочно/Важно: классы CharField, EmailField и т.д. берутся из модуля (ветки) django.forms,
# а не из модуля (ветки) models !!!



#     Используя Forms.py (ФОРМЫ) мы можем задавать проверять данные ЧЕРЕЗ "if form.is_valid():"
# и получать очищенные данные формы ЧЕРЕЗ "form.cleaned_data"

# 1 Вариант - ПРОВЕРКА НА СТОРОНЕ браузера:
# postcode = forms.CharField(label='Почтовый индекс', max_length=6, min_length=6)

# 2 Вариант - ПРОВЕРКА НА СТОРОНЕ СЕРВЕРА - Выдает сообщение об ошибках message="----":
#   Использую стандартные ВАЛИДАТОРЫ - например MinLengthValidator, MaxLengthValidator и т.д.

# postcode = forms.CharField(label='Почтовый индекс',
#                                validators=[
#                                    MinLengthValidator(6, message='Минимум 6 цифр'),
#                                    MaxLengthValidator(6, message='Максимум 6 цифр'),
#                                    ])
#
#
# Справочно - F12 - Просмотреть код HTML страницы и увидеть на ней инструкцию валидатора
#
# Если ничего не трогать, то увидим проверку на стороне браузера - "ВСПЛЫВАЮЩЕЕ окно с сообщением об ошибке":
#
# Если вручную убрать например "required=True" - то увидим ошибку "Обязательное поле" на стороне СЕРВЕРА !!!;
# min_length=2 error_messages={'min_length': 'Слишком короткое имя'} на стороне СЕРВЕРА !!!;
# (сообщением об ошибке над строкой)


# error_messages={'min_length': 'Слишком короткое имя'} - мы можем создавать свои сообщения об ошибках!



# СОЗДАНИЕ СОБСТВЕННЫХ ВАЛИДАТОРОВ (через декоратор @deconstructible):
#
# Например, создадим ВАЛИДАТОР для поля "first_name", который будет проверять - чтобы "ИМЯ" содержало
# только РУССКИЕ БУКВЫ !!!

# Справочно - чтобы импортировать декоратор - "@deconstructible" наводим на него курсор и ДЕРЖИМ !!!
#             ПОЯВИТЬСЯ import deconstructible

@deconstructible
class RussianLettersValidator:
    ALLOWED_CHARS = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя'
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Допускаются только русские буквы.'

    # Справочно - чтобы импортировать ValidationError наводим на него курсор и ДЕРЖИМ !!!
    # #             ПОЯВИТЬСЯ import this name - django.core.exceptions.ValidationError

    def __call__(self, value):
        for char in value:
            if char not in self.ALLOWED_CHARS:
                raise ValidationError(self.message, code=self.code)


class ProfileForm(forms.Form):
    first_name = forms.CharField(label='Имя', min_length=2, max_length=100,           # ПО умолчанию = True (обязательное)
                                  error_messages={'min_length': 'Слишком короткое имя',
                                                  'required': 'Обязательное поле'},
                                  validators=[
                                      RussianLettersValidator(),
                                  ])
    last_name = forms.CharField(label='Фамилия', min_length=2, max_length=100)
    age = forms.IntegerField(label='Возраст', min_value=18, max_value=100)
    phone = forms.CharField(label='Телефон', max_length=20,
                            widget=forms.TextInput(attrs={'placeholder': '+375 (00) 000-00-00'}),
                            error_messages={'max_length': 'Слишком длинный номер телефона',
                                            'required': 'Обязательное поле'})
    # С помощью параметра "initial" можно установить значения по умолчанию (т.е.позволяет определять начальное значение
    # для его отображении на незаполненной форме)
    # postcode = forms.CharField(label='Почтовый индекс', max_length=6, min_length=6)`
    postcode = forms.CharField(label='Почтовый индекс',
                               widget=forms.TextInput(attrs={'placeholder': '000000'}),
                               validators=[
                                   MinLengthValidator(6, message='Минимум 6 цифр'),
                                   MaxLengthValidator(6, message='Максимум 6 цифр'),
                               ])
    about = forms.CharField(label='Комментарий', help_text='Напишите немного о себе',
                            widget=forms.Textarea(attrs={'rows': 5, 'cols': 30}), required=False)
    image = forms.ImageField(label='Изображение', required=False)
    # image = forms.ImageField(label='Изображение', required=False)

# 3 Вариант - ПОЛЬЗОВАТЕЛЬСКАЯ ВАЛИДАЦИЯ мы можем добавить собственные правила валидации, переопределив метод "clean"
# в классе формы или создав методы clean_ < fieldname > для отдельных полей:

    def clean_postcode(self):
        postcode = self.cleaned_data['postcode']
        if not postcode.isdigit():
            raise forms.ValidationError('Почтовый индекс должен содержать только цифры')
        return postcode

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        # if len(first_name) < 2:
        if not first_name.isalpha():
            raise forms.ValidationError('Имя должно содержать только буквы')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise forms.ValidationError('Фамилия должна содержать только буквы')
        return last_name

#  Пояснение: По умолчанию поле CharField использует виджет forms.widgets.TextInput, который создает однострочное
# текстовое поле. Однако если нам надо создать многострочное текстовое поле, то необходимо воспользоваться
# вторым виджетом forms.Textarea:

# 1. Виджеты Django - например "widget=forms.Textarea" можно посмотреть на METANIT (https://metanit.com/python/django/4.2.php)
#    Также в виджетах можно передавать атрибуты - например "rows=5, cols=30"
#    Атрибуты можно передавать через словарь - например "widget=forms.Textarea(attrs={'rows': 5, 'cols': 30})"
#
#     1.1 Widget для полей формы - все виджеты с описаниями в документации на django(https://docs.djangoproject.com/en/3.1/ref/forms/widgets/)
#
# 2. Типы полей формы - все типы с описаниями в документации на django.forms (https://docs.djangoproject.com/en/3.1/ref/forms/fields/)
#      2.1 или на METANIT (https://metanit.com/python/django/4.2.php)


# Примечание:
# в ProfileForm мы не указывали поле "time_created" из class Profile(models.Model)
# По умолчанию Django добавляет поле time_created = models.DateTimeField(auto_now_add=True),


#     Просто ПРИМЕР с сайта Stackoverflow.com:
#
#     Django - проверка формы не выполняется в модальном диалоговом окне bootstrap
#
# class Register(forms.Form):
#     username = forms.CharField(label='', max_length=64, widget=forms.TextInput({'placeholder': 'User Name'}))
#     firstname = forms.CharField(label='', max_length=64, widget=forms.TextInput({'placeholder': 'First Name'}))
#     surname = forms.CharField(label='', max_length=64, widget=forms.TextInput({'placeholder': 'Sur Name / Second Name'}))
#     email = forms.EmailField(label='', max_length=64, widget=forms.TextInput({'placeholder': 'Email'}))
#
#
# При отображении формы в простом HTML-файле проверка формы происходит,
# тогда как в модальном диалоговом окне она НЕ работает.
#
# Мой HTML-код для модального диалогового окна выглядит следующим образом:
#
# <div class="col-md-12 text-center">
#     <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#ApplyJob">Apply for Job</button>
# </div>
#
# <div id="ApplyJob" class="modal fade" role="dialog">
#     <div class="modal-dialog">
#         <div class="modal-content">
#             <div class="modal-header">
#                 <div class="modal-title">
#                     <button type="button" class="close" data-dismiss="modal">&times;</button>
#
#                 </div>
#             </div>
#             <form action="" method="post"> {% csrf_token %}
#                 <div class="modal-body">
#                     {{ form|crispy }}
#
#                 </div>
#                 <div class="modal-footer">
#                     <input type="submit" value="Apply" class="btn btn-primary"/>
#                 </div>
#             </form>
#         </div>
#     </div>
# </div>
#
# Он отображает модальное окно и принимает входные данные, но проверка формы не происходит,
# пожалуйста, помогите мне с этим.