from django.urls import path
from .views import *

urlpatterns = [
    path('product_detail/<int:id>/', product_detail, name='product_detail'),
    path('product_list/', product_list, name='product_list'),
    path('product_search/', product_search, name='product_search'),
    path('cart/', cart, name='cart'),
    path('add_to_cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('remove_cart/<int:id>/', remove_cart, name='remove_cart'),
    path('increament_cart/<int:id>/', increament_cart, name='increament_cart'),
    path('decreament_cart/<int:id>/', decreament_cart, name='decreament_cart'),
    path('checkout/', checkout, name='checkout'),
    path('payment_success/', payment_success, name='payment_success'),
    path('payment_fail/', payment_fail, name='payment_fail'),
    path('payment_cancel/', payment_cancel, name='payment_cancel'),
    path('payment_gateway/', payment_gateway, name='payment_gateway'),
]
