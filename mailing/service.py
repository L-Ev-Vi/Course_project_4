from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from .models import Recipient, Message, Mailing, MailingAttempts


class MailingService:
    """Класс описывающий методы бизнес-логики приложения 'mailing'."""

    @staticmethod
    def get_list_recipients():
        """Метод передаёт список клиентов."""
        if settings.CACHE_ENABLED:
            key = "recipients"
            recipients = cache.get(key)
            if not recipients:
                recipients = Recipient.objects.all()
                cache.set(key, recipients, 60 * 10)
            return recipients
        return Recipient.objects.all()

    @staticmethod
    def get_list_recipients_user(user):
        """Метод передаёт список клиентов конкретного пользователя."""
        if settings.CACHE_ENABLED:
            key = f"recipients_{user}"
            recipients = cache.get(key)
            if not recipients:
                recipients = Recipient.objects.filter(owner=user)
                cache.set(key, recipients, 60 * 2)
            return recipients
        return Recipient.objects.filter(owner=user)

    @staticmethod
    def get_list_messages():
        """Метод передаёт список сообщений."""
        if settings.CACHE_ENABLED:
            key = "messages"
            messages = cache.get(key)
            if not messages:
                messages = Message.objects.all()
                cache.set(key, messages, 60 * 10)
            return messages
        return Message.objects.all()

    @staticmethod
    def get_list_messages_user(user):
        """Метод передаёт список сообщений конкретного пользователя."""
        if settings.CACHE_ENABLED:
            key = f"messages_{user}"
            messages = cache.get(key)
            if not messages:
                messages = Message.objects.filter(owner=user)
                cache.set(key, messages, 60 * 2)
            return messages
        return Message.objects.filter(owner=user)

    @staticmethod
    def get_list_all_mailing():
        """Метод передаёт список всех рассылок."""
        if settings.CACHE_ENABLED:
            key = "all_mailing_lists"
            all_mailing_lists = cache.get(key)
            if not all_mailing_lists:
                all_mailing_lists = Mailing.objects.all()
                cache.set(key, all_mailing_lists, 60 * 1)
            return all_mailing_lists
        return Mailing.objects.all()

    @staticmethod
    def get_list_mailing_published():
        """Метод передаёт список не заблокированных рассылок."""
        if settings.CACHE_ENABLED:
            key = "list_mailing_published"
            list_mailing_published = cache.get(key)
            if not list_mailing_published:
                list_mailing_published = Mailing.objects.filter(publication=True)
                cache.set(key, list_mailing_published, 60 * 1)
            return list_mailing_published
        return Mailing.objects.filter(publication=True)

    @staticmethod
    def get_list_mailing_published_and_launched():
        """Метод передаёт список не заблокированных рассылок со статусом "Запущена"."""
        if settings.CACHE_ENABLED:
            key = "list_mailing_published_and_launched"
            list_mailing_published_and_launched = cache.get(key)
            if not list_mailing_published_and_launched:
                list_mailing_published_and_launched = Mailing.objects.filter(status="Запущена", publication=True)
                cache.set(key, list_mailing_published_and_launched, 60 * 1)
            return list_mailing_published_and_launched
        return Mailing.objects.filter(status="Запущена", publication=True)

    @staticmethod
    def get_list_mailing_published_user(user):
        """Метод передаёт список не заблокированных рассылок пользователя."""
        if settings.CACHE_ENABLED:
            key = f"list_mailing_published_{user}"
            list_mailing_published = cache.get(key)
            if not list_mailing_published:
                list_mailing_published = Mailing.objects.filter(owner=user, publication=True)
                cache.set(key, list_mailing_published, 60 * 1)
            return list_mailing_published
        return Mailing.objects.filter(owner=user, publication=True)

    @staticmethod
    def get_list_mailing_attempts_user(user):
        """Метод передаёт список попыток-рассылок пользователя."""
        if settings.CACHE_ENABLED:
            key = f"mailing_attempts_{user}"
            mailing_attempts = cache.get(key)
            if not mailing_attempts:
                mailing_attempts = MailingAttempts.objects.filter(owner=user)
                cache.set(key, mailing_attempts, 60 * 1)
            return mailing_attempts
        return MailingAttempts.objects.filter(owner=user)

    @staticmethod
    def get_list_mailing_attempts_user_status_successfully(user):
        """Метод передаёт список успешных попыток-рассылок пользователя."""
        if settings.CACHE_ENABLED:
            key = f"mailing_attempts_status_successfully_{user}"
            mailing_attempts_status_successfully = cache.get(key)
            if not mailing_attempts_status_successfully:
                mailing_attempts_status_successfully = MailingAttempts.objects.filter(owner=user, status="Успешно")
                cache.set(key, mailing_attempts_status_successfully, 60 * 1)
            return mailing_attempts_status_successfully
        return MailingAttempts.objects.filter(owner=user, status="Успешно")

    @staticmethod
    def get_list_mailing_attempts_user_status_not_successfully(user):
        """Метод передаёт список успешных попыток-рассылок пользователя."""
        if settings.CACHE_ENABLED:
            key = f"mailing_attempts_status_not_successfully_{user}"
            mailing_attempts_status_not_successfully = cache.get(key)
            if not mailing_attempts_status_not_successfully:
                mailing_attempts_status_not_successfully = MailingAttempts.objects.filter(owner=user, status="Не успешно")
                cache.set(key, mailing_attempts_status_not_successfully, 60 * 1)
            return mailing_attempts_status_not_successfully
        return MailingAttempts.objects.filter(owner=user, status="Не успешно")

    @staticmethod
    def get_mailing(pk):
        """Метод передаёт рассылку."""
        if settings.CACHE_ENABLED:
            key = f"mailing_{pk}"
            mailing = cache.get(key)
            if not mailing:
                mailing = get_object_or_404(Mailing, pk=pk)
                cache.set(key, mailing, 60 * 2)
            return mailing
        return get_object_or_404(Mailing, pk=pk)
