from django.urls import path
from userProfile import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('register/', views.register_user, name='register'),
    path('register/', views.registration_form, name='register_form'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('add-profile/', views.add_profile_user, name='add-profile'),
    path('profile-list/', views.profile_users_list, name='profile-list'),
    path('profile-user/', views.profile_user, name='profile-user'),
    path('delete-profile/', views.delete_profile_user, name='delete-profile'),
]
