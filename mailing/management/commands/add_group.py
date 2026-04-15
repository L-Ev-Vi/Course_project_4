from typing import Any

from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Создание группы 'Менеджеры' с правами доступа."

    def handle(self, *args: Any, **options: Any) -> None:
        """Метод создания группы"""

        # предварительное удаление данных, из таблиц auth_group и auth_permission, перед загрузкой новых
        Group.objects.all().delete()
        Permission.objects.all().delete()

        # сброс инкремента (счётчика 'id' до 1)
        with connection.cursor() as cur:
            cur.execute("ALTER SEQUENCE auth_permission_id_seq RESTART WITH 1")  # чистый SQL запрос
        with connection.cursor() as cur:
            cur.execute("ALTER SEQUENCE auth_group_permissions_id_seq RESTART WITH 1")  # чистый SQL запрос
        with connection.cursor() as cur:
            cur.execute("ALTER SEQUENCE auth_group_id_seq RESTART WITH 1")  # чистый SQL запрос
        # данные операции были выполнены в рамках тестирования и не рекомендуются для массового использования

        call_command("loaddata", "mailing/management/commands/groups_fixture.json", "--ignorenonexistent")
