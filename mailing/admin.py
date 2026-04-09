from django.contrib import admin

from mailing.models import Recipient, Message, Mailing


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    """Класс регистрации и настройки отображения модели 'Recipient' в админке"""

    list_display = (
        "pk",
        "first_name",
        "last_name",
        "email",
        "created_at",
        "owner",
    )
    list_filter = ("owner",)
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Класс регистрации и настройки отображения модели 'Message' в админке"""

    list_display = (
        "pk",
        "subject_letter",
        "created_at",
        "owner",
    )
    list_filter = ("owner",)
    search_fields = (
        "subject_letter",
        "body_letter",
    )


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """Класс регистрации и настройки отображения модели 'Mailing' в админке"""

    list_display = (
        "pk",
        "status",
        "start_time",
        "end_time",
        "owner",
    )
    list_filter = ("owner", "status",)
    search_fields = (
        "start_time",
    )
