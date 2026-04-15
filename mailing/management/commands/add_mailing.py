import zoneinfo
from datetime import timedelta
from typing import Any

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone

from mailing.models import Mailing, MailingAttempts, Message, Recipient
from users.models import UserOfService


class Command(BaseCommand):
    help = "Добавление категорий и продуктов тестирования в базу данных"

    def handle(self, *args: Any, **options: Any) -> None:
        """Метод добавления данных в БД"""

        # предварительное удаление данных из таблиц
        Mailing.objects.all().delete()
        Message.objects.all().delete()
        Recipient.objects.all().delete()
        MailingAttempts.objects.all().delete()

        # сброс инкремента (счётчика 'id' до 1)
        with connection.cursor() as cur:
            cur.execute("ALTER SEQUENCE recipient_id_seq RESTART WITH 1")  # чистый SQL запрос
        with connection.cursor() as cur:
            cur.execute("ALTER SEQUENCE message_id_seq RESTART WITH 1")  # чистый SQL запрос
        with connection.cursor() as cur:
            cur.execute("ALTER SEQUENCE mailing_id_seq RESTART WITH 1")  # чистый SQL запрос
        with connection.cursor() as cur:
            cur.execute("ALTER SEQUENCE mailing_attempts_id_seq RESTART WITH 1")  # чистый SQL запрос
        # данные операции были выполнены в рамках тестирования и не рекомендуются для массового использования

        owner = UserOfService.objects.get(pk=1)

        recipient_data = {"email": "test@exmpl.com", "first_name": "Test", "last_name": "Tests", "owner": owner}
        recipient = Recipient.objects.create(**recipient_data)

        message_data = {"subject_letter": "Test1", "body_letter": "Text", "owner": owner}
        message = Message.objects.create(**message_data)

        timezone.activate(zoneinfo.ZoneInfo("Europe/Moscow"))
        start_time = timezone.localtime()
        end_time = start_time + timedelta(minutes=5)  # Добавление 5 минут

        mailing_data = {
            "start_time": start_time,
            "end_time": end_time,
            "status": "Запущена",
            "message": message,
            "owner": owner,
        }
        mailing = Mailing.objects.create(**mailing_data)
        mailing.recipient.add(recipient)
        mailing.save()

        subject = mailing.message.subject_letter
        message = mailing.message.body_letter
        try:
            recipient_list = [recipient.email]
            # отправка письма на адрес электронной почты клиента
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        except Exception as server_response:
            # попытка рассылки и добавление её в БД
            mailing_attempts = MailingAttempts.objects.create(
                status="Не успешно",
                server_response=f"Error: {server_response}",
                mailing=mailing,
                owner=mailing.owner,
            )
        else:
            mailing_attempts = MailingAttempts.objects.create(
                status="Успешно", server_response="Отправлено", mailing=mailing, owner=mailing.owner
            )
        self.stdout.write(self.style.SUCCESS(f"Попытка рассылки со статусом: {mailing_attempts.status}"))
