import secrets

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from mailing.service import MailingService
from users.forms import (
    AuthenticationUserOfService,
    ChangeUserOfService,
    ChangeUsersOfService,
    FormUserOfService,
    PasswordChangeUserOfServiceForms,
    PasswordResetConfirmForm,
    PasswordResetUserForm,
)
from users.models import UserOfService


class MyLogin(LoginView):
    """Классовое представление для авторизации пользователей."""

    form_class = AuthenticationUserOfService  # указываем форму
    template_name = "users/login_user.html"  # определяем шаблон


class MyLogout(LogoutView):
    """Классовое представление для выхода пользователей из системы."""

    pass


@method_decorator(cache_page(60 * 60), name="dispatch")
class Verification(TemplateView):
    """Классовое представление принимающее GET запрос,
    и возвращающее страницу с сообщением об необходимости подтверждения почты."""

    template_name = "users/verification.html"  # определяем шаблон


class CreateUser(CreateView):
    """Классовое представление для регистрации пользователей."""

    model = UserOfService  # определяем модель
    form_class = FormUserOfService  # указываем форму
    template_name = "users/register_user.html"  # определяем шаблон
    success_url = reverse_lazy("users:verification")  # определяем URL-адрес для перехода

    def form_valid(self, form):
        """Расширение метода валидации формы, через отправку письма для подтверждения адреса электронной почты,
        после успешной валидации формы."""
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        self.send_welcome_email(user.email, url)
        return super().form_valid(form)

    def send_welcome_email(self, user_email, url):
        """Метод отправки письма для подтверждения адреса электронной почты."""
        subject = "Добро пожаловать на наш сервис!"
        message = f"Для продолжения регистрации подтвердите почту перейдя по ссылке - {url}"
        recipient_list = [user_email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


def email_verification(request, token):
    """Функция верификации пользователя по 'email'."""
    user = get_object_or_404(UserOfService, token=token)
    user.is_active = True
    user.save()
    login(request, user)
    return redirect(reverse("mailing:index"))


class UpdateUser(UpdateView):
    """Классовое представление для редактирования пользователя."""

    model = UserOfService  # определяем модель
    form_class = ChangeUserOfService  # указываем форму
    template_name = "users/register_user.html"  # определяем шаблон

    def get_success_url(self):
        """Метод перенаправления на страницу 'Пользователя' после его(ё) редактирования."""
        if self.request.user == self.object:
            return reverse_lazy("users:detail_user")
        else:
            return reverse_lazy("users:user_information", kwargs={"pk": self.object.pk})

    def get_form_class(self):
        """Метод выполняющий проверку прав доступа на редактирование 'Пользователя'."""
        user = self.request.user
        if user == self.object:
            return ChangeUserOfService
        elif user.has_perm("users.can_inactive_users"):
            return ChangeUsersOfService
        else:
            raise PermissionDenied


class PasswordsChangeUser(PasswordChangeView):
    """Классовое представление для смены пароля пользователя."""

    model = UserOfService  # определяем модель
    form_class = PasswordChangeUserOfServiceForms  # указываем форму
    template_name = "users/change-password.html"  # определяем шаблон
    success_url = reverse_lazy("users:change_profile")  # определяем URL-адрес для перехода

    def get_success_url(self):
        """Метод перенаправления на страницу 'Редактирования пользователя'."""
        return reverse_lazy("users:change_profile", kwargs={"pk": self.request.user.pk})

    def form_valid(self, form):
        """Расширение метода валидации формы, через отправку письма после успешного изменения пароля."""
        user = form.save()
        user.save()
        self.send_email(user.email)
        return super().form_valid(form)

    def send_email(self, user_email):
        """Метод отправки письма после успешного изменения пароля."""
        subject = "Уведомление о смене пароля!"
        message = "Ваш пароль был успешно изменён!"
        recipient_list = [user_email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


class PasswordResetUser(PasswordResetView):
    """Классовое представление для восстановления пароля пользователя."""

    form_class = PasswordResetUserForm  # указываем форму
    template_name = "users/password_reset_form.html"  # определяем шаблон
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:recovery")  # определяем URL-адрес для перехода


@method_decorator(cache_page(60 * 60), name="dispatch")
class Recovery(TemplateView):
    """Классовое представление принимающее GET запрос,
    и возвращающее страницу с сообщением об необходимости перейти в почту."""

    template_name = "users/recovery.html"  # определяем шаблон


class PasswordResetConfirmUser(PasswordResetConfirmView):
    """Классовое представление для ввода нового пароля пользователя."""

    form_class = PasswordResetConfirmForm  # указываем форму
    template_name = "users/password_reset_confirm.html"  # определяем шаблон
    success_url = reverse_lazy("users:password_reset_complete")  # определяем URL-адрес для перехода


class PasswordResetCompleteUser(PasswordResetCompleteView):
    """Классовое представление для уведомления о смене пароля пользователя."""

    template_name = "users/password_reset_complete.html"  # определяем шаблон


class DetailUser(LoginRequiredMixin, DetailView):
    """Классовое представление принимающее GET запрос и возвращающее страницу 'Пользователя'."""

    model = UserOfService  # определяем модель
    template_name = "users/detail_user.html"  # определяем шаблон
    context_object_name = "current_user"  # определяем переменную для использования в шаблоне

    def get_context_data(self, **kwargs):
        """Переопределённый метод 'get_context_data'. Метод передаёт количество рассылок пользователя."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["number_mailing_lists"] = MailingService.get_list_mailing_published_user(user).count()
        return context

    def get_object(self, queryset=None):
        return self.request.user


@method_decorator(cache_page(60 * 1), name="dispatch")
class ListUsers(ListView):
    """Классовое представление принимающее GET запрос и возвращающее страницу с зарегистрированными пользователями."""

    model = UserOfService  # определяем модель
    template_name = "users/list_users.html"  # определяем шаблон
    context_object_name = "users"  # определяем переменную для использования в шаблоне
    paginate_by = 18  # определяем количество пользователей на странице

    def get_queryset(self):
        """Переопределённый метод 'get_queryset'.
        Метод передаёт список пользователей при условии, что у пользователя есть права менеджера."""
        list_users = []
        user = self.request.user
        if user.has_perm("mailing.can_unpublish_mailing"):
            for user in UserOfService.objects.all():
                if not user.has_perm("mailing.can_unpublish_mailing"):
                    list_users.append(user)
            return list_users
        else:
            return PermissionDenied


@method_decorator(cache_page(60 * 5), name="dispatch")
class DetailUserOfService(LoginRequiredMixin, DetailView):
    """Классовое представление принимающее GET запрос и возвращающее страницу 'Пользователя'."""

    model = UserOfService  # определяем модель
    template_name = "users/detail_user.html"  # определяем шаблон
    context_object_name = "current_user"  # определяем переменную для использования в шаблоне

    def get_context_data(self, **kwargs):
        """Переопределённый метод 'get_context_data'. Метод передаёт количество рассылок пользователя."""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context["number_mailing_lists"] = MailingService.get_list_mailing_published_user(user).count()
        return context
