from django.contrib import admin

from users.models import UserOfService


@admin.register(UserOfService)
class UserOfServiceAdmin(admin.ModelAdmin):
    """Класс регистрации и настройки отображения модели 'UserOfService' в админке"""

    list_display = (
        "email",
        "first_name",
        "last_name",
    )
    search_fields = ("email",)
