from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('home/', login_, name='login_'),
    path('', about, name='about'),
    path('logout/', logout_, name='logout_'),
    path('profile/', profile, name='profile'),
    path('update_profile/', update_profile, name='update_profile'),
    path('reset_pass/', reset_pass, name='reset_pass'),
    path('forgot_pass/', forgot_pass, name='forgot_pass'),
    path('new_password/', new_password, name='new_password'),
]