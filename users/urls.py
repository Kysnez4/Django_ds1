#users
from django.urls import path

from users.views import CustomUserLogin, CustomUserLogout, RegisterView

urlpatterns = [
    path('login/', CustomUserLogin.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', CustomUserLogout.as_view(), name='logout'),
]