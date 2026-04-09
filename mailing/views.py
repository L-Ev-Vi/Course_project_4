from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.views.generic import DetailView, View, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Recipient, Message, Mailing, MailingAttempts
from .forms import FormRecipient, FormMessage, FormMailing, FormMailingPublication
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, render, redirect
from users.models import UserOfService


# Recipient

class ListRecipients(LoginRequiredMixin, ListView):
    """Классовое представление принимающее GET запрос
    и возвращающее страницу со списком потенциальных 'Получателей рассылок'."""

    model = Recipient  # определяем модель
    template_name = "mailing/list_recipients.html"  # определяем шаблон
    context_object_name = "recipients"  # определяем переменную для использования в шаблоне
    paginate_by = 12  # определяем количество продуктов на странице

    def get_queryset(self):
        """Переопределённый метод 'get_queryset'.
        Метод отбирает только тех получателей к которым у пользователя есть доступ."""
        user = self.request.user
        if user.has_perm("mailing.can_unpublish_mailing"):
            return Recipient.objects.all()
        else:
            return Recipient.objects.filter(owner=user)


class CreateRecipient(LoginRequiredMixin, CreateView):
    """Классовое представление принимающее GET и POST запрос
    и возвращающее страницу для добавления 'Получателя рассылок'."""

    model = Recipient  # определяем модель
    form_class = FormRecipient  # указываем форму
    template_name = "mailing/add_recipient.html"  # определяем шаблон
    success_url = reverse_lazy("mailing:list_recipients")  # определяем URL-адрес для перехода

    def form_valid(self, form):
        """Метод определения автора 'Получателя рассылки' после успешной валидации формы."""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DetailRecipient(LoginRequiredMixin, DetailView):
    """Классовое представление принимающее GET запрос и возвращающее страницу 'Получателя рассылки'."""

    model = Recipient  # определяем модель
    template_name = "mailing/detail_recipient.html"  # определяем шаблон
    context_object_name = "recipient"  # определяем переменную для использования в шаблоне


class UpdateRecipient(LoginRequiredMixin, UpdateView):
    """Классовое представление принимающее GET и POST запрос и возвращающее страницу редактирования 'Получателя рассылки'."""

    model = Recipient  # определяем модель
    form_class = FormRecipient  # указываем форму
    template_name = "mailing/add_recipient.html"  # определяем шаблон

    def get_success_url(self):
        """Метод перенаправления на страницу 'Получателя рассылки' после его(ё) редактирования."""
        return reverse_lazy("mailing:detail_recipient", kwargs={"pk": self.object.pk})

    def get_form_class(self):
        """Метод выполняющий проверку прав доступа на редактирование 'Получателя рассылки'."""
        user = self.request.user
        if user == self.object.owner:
            return FormRecipient
        else:
            raise PermissionDenied


class DeleteRecipient(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Классовое представление принимающее GET и POST запросы,
        и возвращающее страницу подтверждения об удалении 'Получателя рассылки'."""

    model = Recipient  # определяем модель
    template_name = "mailing/delete_recipient.html"  # определяем шаблон
    success_url = reverse_lazy("mailing:list_recipients")  # определяем URL-адрес для перехода
    context_object_name = "recipient"  # определяем переменную для использования в шаблоне

    def test_func(self):
        """Метод проверки условия на доступ к представлению."""
        return self.request.user.has_perm("mailing.delete_recipient") or self.get_object().owner == self.request.user


# Message

class ListMessage(LoginRequiredMixin, ListView):
    """Классовое представление принимающее GET запрос и возвращающее страницу с сообщениями."""

    model = Message  # определяем модель
    template_name = "mailing/list_messages.html"  # определяем шаблон
    context_object_name = "messages"  # определяем переменную для использования в шаблоне
    paginate_by = 12  # определяем количество продуктов на странице

    def get_queryset(self):
        """Переопределённый метод 'get_queryset'.
        Метод отбирает только те сообщения к которым у пользователя есть доступ."""
        user = self.request.user
        if user.has_perm("mailing.can_unpublish_mailing"):
            return Message.objects.all()
        else:
            return Message.objects.filter(owner=user)


class CreateMessage(LoginRequiredMixin, CreateView):
    """Классовое представление принимающее GET и POST запрос и возвращающее страницу для добавления 'Сообщения'."""

    model = Message  # определяем модель
    form_class = FormMessage  # указываем форму
    template_name = "mailing/add_message.html"  # определяем шаблон
    success_url = reverse_lazy("mailing:list_messages")  # определяем URL-адрес для перехода

    def form_valid(self, form):
        """Метод определения автора сообщения после успешной валидации формы."""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DetailMessage(LoginRequiredMixin, DetailView):
    """Классовое представление принимающее GET запрос и возвращающее страницу 'Сообщения'."""

    model = Message  # определяем модель
    template_name = "mailing/detail_message.html"  # определяем шаблон
    context_object_name = "message"  # определяем переменную для использования в шаблоне


class UpdateMessage(LoginRequiredMixin, UpdateView):
    """Классовое представление принимающее GET и POST запрос и возвращающее страницу редактирования 'Сообщения'."""

    model = Message  # определяем модель
    form_class = FormMessage  # указываем форму
    template_name = "mailing/add_message.html"  # определяем шаблон

    def get_success_url(self):
        """Метод перенаправления на страницу 'Сообщения' после его(ё) редактирования."""
        return reverse_lazy("mailing:detail_message", kwargs={"pk": self.object.pk})

    def get_form_class(self):
        """Метод выполняющий проверку прав доступа, на редактирование 'Сообщения'."""
        user = self.request.user
        if user == self.object.owner:
            return FormMessage
        else:
            raise PermissionDenied


class DeleteMessage(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Классовое представление принимающее GET и POST запросы,
        и возвращающее страницу подтверждения об удалении 'Сообщения'."""

    model = Message  # определяем модель
    template_name = "mailing/delete_message.html"  # определяем шаблон
    success_url = reverse_lazy("mailing:list_messages")  # определяем URL-адрес для перехода
    context_object_name = "message"  # определяем переменную для использования в шаблоне

    def test_func(self):
        """Метод проверки условия на доступ к представлению."""
        return self.request.user.has_perm("mailing.delete_message") or self.get_object().owner == self.request.user


# Mailing

class IndexMailing(ListView):
    """Классовое представление принимающее GET запрос и возвращающее главную страницу с рассылками."""

    model = Mailing  # определяем модель
    template_name = "mailing/index.html"  # определяем шаблон
    context_object_name = "mailings"  # определяем переменную для использования в шаблоне
    paginate_by = 6  # определяем количество продуктов на странице

    def get_context_data(self, *, object_list=None, **kwargs):
        """Переопределённый метод 'get_context_data'. Метод передаёт общее количество рассылок,
        количество активных рассылок и общее число клиентов в системе."""
        context = super().get_context_data(**kwargs)
        context["number_mailings"] = Mailing.objects.filter(publication=True).count()
        context["number_mailings_active"] = Mailing.objects.filter(status="Запущена", publication=True).count()
        context["number_recipientes"] = Recipient.objects.all().count()
        return context

    def get_queryset(self):
        """Переопределённый метод 'get_queryset'.
        Метод отбирает только те рассылки к которым у пользователя есть доступ."""
        user = self.request.user
        users = UserOfService.objects.all()
        if user.has_perm("mailing.can_unpublish_mailing"):
            return Mailing.objects.all()
        elif user in users:
            return Mailing.objects.filter(owner=user, publication=True)
        else:
            return Mailing.objects.filter(publication=True)


class CreateMailing(LoginRequiredMixin, CreateView):
    """Классовое представление принимающее GET и POST запрос и возвращающее страницу для добавления 'Рассылок'."""

    model = Mailing  # определяем модель
    form_class = FormMailing  # указываем форму
    template_name = "mailing/add_mailing.html"  # определяем шаблон
    success_url = reverse_lazy("mailing:index")  # определяем URL-адрес для перехода

    def form_valid(self, form):
        """Метод определения автора 'Рассылки' после успешной валидации формы."""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DetailMailing(LoginRequiredMixin, DetailView):
    """Классовое представление принимающее GET запрос и возвращающее страницу 'Получателя рассылки'."""

    model = Mailing  # определяем модель
    template_name = "mailing/detail_mailing.html"  # определяем шаблон
    context_object_name = "mailing"  # определяем переменную для использования в шаблоне

    def get_object(self, queryset=None):
        """Переопределения метода 'get_object' для проверки и обновления статуса рассылки."""
        obj = super().get_object(queryset)
        obj.update_status()
        obj.save()
        return obj

    def get_context_data(self, *, object_list=None, **kwargs):
        """Переопределённый метод 'get_context_data'. Метод передаёт общее количество рассылок,
        количество активных рассылок и общее число клиентов в системе."""
        context = super().get_context_data(**kwargs)
        mailing = self.object
        recipient = mailing.recipient
        context["number_mailings"] = recipient.count()
        context["list_recipients"] = recipient.all()
        return context


class UpdateMailing(LoginRequiredMixin, UpdateView):
    """Классовое представление принимающее GET и POST запрос и возвращающее страницу редактирования 'Сообщения'."""

    model = Mailing  # определяем модель
    form_class = FormMailing  # указываем форму
    template_name = "mailing/add_mailing.html"  # определяем шаблон

    def get_success_url(self):
        """Метод перенаправления на страницу 'Рассылки' после его(ё) редактирования."""
        return reverse_lazy("mailing:detail_mailing", kwargs={"pk": self.object.pk})

    def get_form_class(self):
        """Метод выполняющий проверку прав доступа на редактирование 'Рассылки'."""
        user = self.request.user
        if user == self.object.owner:
            return FormMailing
        elif user.has_perm("mailing.can_unpublish_mailing"):
            return FormMailingPublication
        else:
            raise PermissionDenied


class DeleteMailing(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Классовое представление принимающее GET и POST запросы,
        и возвращающее страницу подтверждения об удалении 'Сообщения'."""

    model = Mailing  # определяем модель
    template_name = "mailing/delete_mailing.html"  # определяем шаблон
    success_url = reverse_lazy("mailing:index")  # определяем URL-адрес для перехода
    context_object_name = "mailing"  # определяем переменную для использования в шаблоне

    def test_func(self):
        """Метод проверки условия на доступ к представлению."""
        return self.request.user.has_perm("mailing.delete_mailing") or self.get_object().owner == self.request.user


# MailingAttempts

class SendingMessages(View):
    """Классовое представление выполняет проверку статуса рассылки,
    перед переходом на страницу ручного запуска рассылки."""

    def get(self, request, pk):
        """Метод перекидывает на страницу согласно статусу рассылки"""
        mailing = get_object_or_404(Mailing, pk=pk)
        if mailing.status in ("Создана", "Завершена"):
            recipient = mailing.recipient
            number_mailings = recipient.count()
            list_recipients = recipient.all()
            context = {"mailing": mailing,
                       "error_message": "Отправка рассылки не разрешена из-за временных ограничений!",
                       "number_mailings": number_mailings, "list_recipients": list_recipients}
            return render(request, "mailing/detail_mailing.html", context)
        return redirect(reverse("mailing:create_sending_messages", kwargs={"pk": pk}))


class CreateSendingMessages(View):
    """Классовое представление для запуска рассылки."""

    def get(self, request, pk):
        """Рендит страницу для запуска рассылки"""
        mailing = get_object_or_404(Mailing, pk=pk)
        recipient = mailing.recipient
        list_recipients = recipient.all()
        context = {"mailing": mailing, "list_recipients": list_recipients, "transition": True}
        return render(request, "mailing/create_sending_messages.html", context)

    def post(self, request, pk):
        """Метод выполняет рассылку сообщений и сохраняет результат рассылки в БД."""
        mailing = get_object_or_404(Mailing, pk=pk)
        recipient = mailing.recipient
        recipients = recipient.all()
        subject = mailing.message.subject_letter
        message = mailing.message.body_letter
        for recipient in recipients:
            try:
                recipient_list = [recipient.email]
                # отправка письма на адрес электронной почты клиента
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
            except Exception as server_response:
                # попытка рассылки и добавление её в БД
                MailingAttempts.objects.create(status="Не успешно", server_response=f"Error: {server_response}",
                                               mailing=mailing, owner=mailing.owner)
            else:
                MailingAttempts.objects.create(status="Успешно", server_response="Отправлено",
                                               mailing=mailing, owner=mailing.owner)
        message = "Рассылка выполнена! С результатами рассылки можно ознакомится в разделе 'Статистика рассылок'."
        number_mailings = mailing.recipient.all().count()
        list_recipients = mailing.recipient.all()
        context = {"mailing": mailing, "message": message,
                   "number_mailings": number_mailings, "list_recipients": list_recipients}
        return render(request, "mailing/detail_mailing.html", context)


class MailingStatistics(LoginRequiredMixin, ListView):
    """Возвращает страницу с отчётом по рассылкам конкретного пользователя."""

    model = MailingAttempts  # определяем модель
    template_name = "mailing/mailing_statistics.html"  # определяем шаблон
    context_object_name = "attempts"  # определяем переменную для использования в шаблоне

    def get_queryset(self):
        """Переопределённый метод 'get_queryset'.
        Метод отбирает только те попытки рассылок к которым относятся к пользователю."""
        user = self.request.user
        return MailingAttempts.objects.filter(owner=user)

    def get_context_data(self, *, object_list=None, **kwargs):
        """Переопределённый метод 'get_context_data'. Метод передаёт количество рассылок,
        количество успешных и не успешных рассылок и общее число клиентов пользователя."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["successful_mailing_lists"] = MailingAttempts.objects.filter(owner=user, status="Успешно").count()
        context["unsuccessful_mailing_lists"] = MailingAttempts.objects.filter(owner=user, status="Не успешно").count()
        context["list_recipients"] = Recipient.objects.filter(owner=user).count()
        context["list_messages"] = Message.objects.filter(owner=user).count()
        return context
