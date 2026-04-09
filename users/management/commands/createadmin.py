from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Создание Администратора, обнуление id и удаление все существующих пользователей."

    def handle(self, *args, **options):
        """Метод добавления данных в БД"""
        User = get_user_model()

        User.objects.all().delete()  # предварительное удаление данных из таблицы users перед созданием администратора.

        # сброс инкремента (счётчика 'id' до 1)
        with connection.cursor() as cur:
            cur.execute("ALTER TABLE users ALTER COLUMN id RESTART SET START 1")  # чистый SQL запрос
            # данные операции были выполнены в рамках тестирования и не рекомендуются для массового использования

        User = get_user_model()
        user = User.objects.create(email="admin@mail.ru", first_name="Admin", last_name="Admine")
        user.set_password("asd1234zxc")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS("'Admin' успешно создан!"))
