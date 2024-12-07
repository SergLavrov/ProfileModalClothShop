from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='get-products/', permanent=True)),
    path('get-products/', views.get_products, name='get-products'), # Одна и та же view с разными url-адресами !
    # path('<int:category_id>/get-products/', views.get_products, name='products-by-category'),  # IF category_id !!!
    path('<int:season_id>/get-products/', views.get_products, name='products-by-category'),

    path('get-products-list/', views.get_products_list, name='get-products-list'),

    path('add-product/', views.add_product, name='add-product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete-product'),

    path('product-details/<int:product_id>/', views.product_details, name='product-details'),

    path('get-sorted/', views.get_sorted_products, name='get-sorted'),

    path('checkbox/', views.checkbox_products, name='checkbox-products'),

    # path('get-products-by-filter/<str:сonfig>/<str:value>/', views.get_products_by_filter, name='get-products-by-filter'),
    # path('<str:сonfig>, <str:value>/get-products-by-filter/', views.get_products_by_filter, name='get-products-by-filter'),
]
