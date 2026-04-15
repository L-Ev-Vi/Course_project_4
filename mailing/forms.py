from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from formset.widgets import DateTimeInput

from mailing.models import Mailing, Message, Recipient


class MixinStyle:
    """Класс-миксин задающий стиль для формы."""

    def __init__(self, *args, **kwargs):
        """Метод стилизации полей формы."""
        super().__init__(*args, **kwargs)
        for key, value in self.fields.items():
            if isinstance(value, bool):
                self.fields[key].widget.attrs.update({"class": "form-check-input"})
            else:
                self.fields[key].widget.attrs.update({"class": "form-control"})


class FormRecipient(MixinStyle, forms.ModelForm):
    """Класс представляющий форму для добавления и редактирования получателей рассылок."""

    class Meta:
        """Клас для добавления данных к форме."""

        model = Recipient  # определяем модель
        fields = [
            "email",
            "first_name",
            "last_name",
            "patronymic",
            "comment",
        ]


class FormMessage(MixinStyle, forms.ModelForm):
    """Класс представляющий форму для добавления и редактирования сообщений."""

    class Meta:
        """Клас для добавления данных к форме."""

        model = Message  # определяем модель
        fields = [
            "subject_letter",
            "body_letter",
        ]


class FormMailing(MixinStyle, forms.ModelForm):
    """Класс представляющий форму для добавления и редактирования рассылок."""

    class Meta:
        """Клас для добавления данных к форме."""

        model = Mailing  # определяем модель
        fields = ["message", "start_time", "end_time", "recipient"]
        localized_fields = (
            "start_time",
            "end_time",
        )

        # recipients = forms.ModelMultipleChoiceField(queryset=Recipient.objects.all())

        widgets = {
            "start_time": DateTimeInput,
            "end_time": DateTimeInput,
        }

    def clean(self):
        """Метод валидации даты начала и окончания рассылки. Метод исключает конфликт времени."""
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        current_datetime = timezone.now()
        if start_time < current_datetime:
            raise ValidationError("Дата начала рассылки не может быть в прошлом!")
        elif end_time < current_datetime:
            raise ValidationError("Дата окончания рассылки не может быть в прошлом!")
        elif end_time <= start_time:
            raise ValidationError("Дата начала рассылки должна быть раньше даты её окончания!")
        return cleaned_data


class FormMailingPublication(forms.ModelForm):
    """Класс представляющий форму для отключения рассылки."""

    class Meta:
        """Клас для добавления данных к форме."""

        model = Mailing  # определяем модель
        fields = ["publication"]

    def __init__(self, *args, **kwargs) -> None:
        """Метод стилизации полей формы."""
        super().__init__(*args, **kwargs)
        self.fields["publication"].widget.attrs.update({"class": "form-check-input"})
