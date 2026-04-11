from django.conf import settings
from django.db import models
from django.utils import timezone


class Recipient(models.Model):
    """Класс описывающий структуру таблицы с получателями рассылок."""

    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    first_name = models.CharField(max_length=50, verbose_name="Имя", help_text="Укажите имя!")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия", help_text="Укажите фамилию!")
    patronymic = models.CharField(max_length=50, blank=True, null=True, verbose_name="Отчество",
                                  help_text="Не обязательно к заполнению!")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий", help_text="Комментарий")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор"
    )

    def __str__(self) -> str:
        """Метод определяет строковое представление объекта."""
        return (f"{self.last_name} {self.first_name} \n"
                f"email: {self.email}")

    class Meta:
        """Клас который добавляет метаданные к модели Category."""

        verbose_name = "Получатель рассылок"
        verbose_name_plural = "Получатели рассылок"
        ordering = ["-created_at"]
        db_table = "recipient"


class Message(models.Model):
    """Класс описывающий структуру таблицы с сообщениями."""

    subject_letter = models.CharField(max_length=100, verbose_name="Тема письма", help_text="Укажите тему письма")
    body_letter = models.TextField(blank=True, null=True, verbose_name="Тело письма",
                                   help_text="Укажите содержание письма")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор"
    )

    def __str__(self) -> str:
        """Метод определяет строковое представление объекта."""
        return f"{self.subject_letter} : {self.created_at}"

    class Meta:
        """Клас который добавляет метаданные к модели Category."""

        verbose_name = "Письмо"
        verbose_name_plural = "Письма"
        ordering = ["-created_at"]
        db_table = "message"


class Mailing(models.Model):
    """Класс описывающий структуру таблицы рассылок."""

    start_time = models.DateTimeField(default=timezone.now, verbose_name="Начала рассылки",
                                      help_text="Дата и время начало рассылки.")
    end_time = models.DateTimeField(verbose_name="Окончание рассылки", help_text="Дата и время окончания рассылки.")
    status = models.CharField(max_length=10, default="Создана", verbose_name="Статус")
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, related_name="message",
                                verbose_name="Сообщение")
    recipient = models.ManyToManyField(Recipient, related_name="recipients", verbose_name="Получатели")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    publication = models.BooleanField(default=True, verbose_name="Признак публикации")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор"
    )

    def update_status(self):
        """Функция проверки статуса рассылки писем."""
        current_datetime = timezone.localtime(timezone.now())
        if current_datetime < self.start_time:
            self.status = "Создана"
        elif current_datetime > self.end_time:
            self.status = "Завершена"
        else:
            self.status = "Запущена"

    def __str__(self) -> str:
        """Метод определяет строковое представление объекта."""
        return f"Рассылка №{self.pk}"

    class Meta:
        """Клас который добавляет метаданные к модели Category."""

        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["-created_at"]
        db_table = "mailing"
        permissions = [
            ("can_unpublish_mailing", "Can unpublish mailing"),
        ]


class MailingAttempts(models.Model):
    """Класс описывающий структуру таблицы попытки рассылок."""

    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    status = models.CharField(max_length=12, verbose_name="Статус")
    server_response = models.TextField(verbose_name="Ответ почтового сервиса.")
    mailing = models.ForeignKey(Mailing, on_delete=models.SET_NULL, null=True, related_name="mailings",
                                verbose_name="Рассылка")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор"
    )

    def __str__(self) -> str:
        """Метод определяет строковое представление объекта."""
        return f"{self.mailing.message.subject_letter} | {self.status} | {self.server_response}"

    class Meta:
        """Клас который добавляет метаданные к модели Category."""

        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ["-attempt_time"]
        db_table = "mailing_attempts"
