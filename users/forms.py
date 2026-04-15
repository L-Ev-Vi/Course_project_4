from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserChangeForm,
    UserCreationForm,
)

from mailing.forms import MixinStyle
from users.models import UserOfService


class FormUserOfService(MixinStyle, UserCreationForm):
    """Класс представляющий форму для регистрации пользователей."""

    usable_password = None

    class Meta(UserCreationForm):
        model = UserOfService
        fields = ["email", "first_name", "last_name", "country", "phone_number", "avatar"]


class AuthenticationUserOfService(MixinStyle, AuthenticationForm):
    """Класс представляющий форму для входа пользователя в систему."""

    pass


class ChangeUserOfService(UserChangeForm):
    """Класс представляющий форму для редактирования пользователей."""

    class Meta(UserChangeForm):
        model = UserOfService
        fields = [
            "email",
            "first_name",
            "last_name",
            "country",
            "phone_number",
            "avatar",
            "password",
        ]

    def __init__(self, *args, **kwargs) -> None:
        """Метод стилизации полей формы."""
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control", "aria-label": "E-mail"})
        self.fields["first_name"].widget.attrs.update({"class": "form-control", "placeholder": "Имя"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control", "placeholder": "Фамилия"})
        self.fields["country"].widget.attrs.update({"class": "form-select", "placeholder": "Страна"})
        self.fields["phone_number"].widget.attrs.update({"class": "form-control", "placeholder": "Номер телефона"})
        self.fields["avatar"].widget.attrs.update({"class": "form-control", "accept": "/media/*"})
        self.fields["password"].widget = forms.HiddenInput()


class PasswordChangeUserOfServiceForms(MixinStyle, PasswordChangeForm):
    """Класс представляющий форму для смены пароля пользователя."""

    pass


class ChangeUsersOfService(UserChangeForm):
    """Класс представляющий форму для блокировки пользователей."""

    class Meta(UserChangeForm.Meta):
        model = UserOfService
        fields = [
            "is_active",
        ]

    def __init__(self, *args, **kwargs) -> None:
        """Метод стилизации полей формы."""
        super().__init__(*args, **kwargs)
        self.fields["is_active"].widget.attrs.update({"class": "form-check-input"})
        self.fields["password"].widget = forms.HiddenInput()


class PasswordResetUserForm(MixinStyle, PasswordResetForm):
    """Класс представляющий форму для ввода почты при восстановлении пароля пользователя."""

    pass


class PasswordResetConfirmForm(MixinStyle, SetPasswordForm):
    """Класс представляющий форму для ввода нового пароля при восстановлении пароля пользователя."""

    pass
