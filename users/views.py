from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER
from users.forms import RegisterUserForm, LoginUserForm


# Create your views here.
class CustomUserLogin(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('home')


class CustomUserLogout(LogoutView):
    next_page = reverse_lazy('home')


class RegisterView(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в наш сервис'
        message = 'Спасибо, что зарегистрировались в нашем сервисе!'
        recipient_list = [user_email]
        send_mail(subject,
                  message,
                  EMAIL_HOST_USER,
                  recipient_list,
                  fail_silently=False,
                  )
