from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('send_mail/', send_mail, name='send_mail'),
    path('signup_otp/', signup_otp, name='signup_otp'),
    path('register/', user_register, name='register'),
]
