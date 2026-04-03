from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class UserOfService(AbstractUser):
    """Класс определяющий модель пользователя"""
    username = None

    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    phone_number = PhoneNumberField(blank=True, null=True, verbose_name="Номер телефона")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Изображение")
    country = CountryField(blank_label="(Выберите страну)", blank=True, null=True, verbose_name="Страна")
    token = models.CharField(max_length=100, verbose_name="Токин", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.last_name} {self.first_name} email: {self.email}"

    class Meta:
        """Класс, который добавляет метаданные к модели UserOfService."""

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]
        db_table = "users"
        permissions = [
            ("can_inactive_users", "Can inactive users"),
        ]
