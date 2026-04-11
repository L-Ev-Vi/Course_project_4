from django.urls import path

from mailing import views
from mailing.apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [

    path("add_recipient/", views.CreateRecipient.as_view(), name="add_recipient"),
    path("detail_recipient/<int:pk>/", views.DetailRecipient.as_view(), name="detail_recipient"),
    path("update_recipient/<int:pk>/", views.UpdateRecipient.as_view(), name="update_recipient"),
    path("delete_recipient/<int:pk>/", views.DeleteRecipient.as_view(), name="delete_recipient"),
    path("list_recipients/", views.ListRecipients.as_view(), name="list_recipients"),

    path("add_message/", views.CreateMessage.as_view(), name="add_message"),
    path("detail_message/<int:pk>/", views.DetailMessage.as_view(), name="detail_message"),
    path("update_message/<int:pk>/", views.UpdateMessage.as_view(), name="update_message"),
    path("delete_message/<int:pk>/", views.DeleteMessage.as_view(), name="delete_message"),
    path("list_messages/", views.ListMessage.as_view(), name="list_messages"),

    path("", views.IndexMailing.as_view(), name="index"),

    path("add_mailing/", views.CreateMailing.as_view(), name="add_mailing"),
    path("detail_mailing/<int:pk>/", views.DetailMailing.as_view(), name="detail_mailing"),
    path("update_mailing/<int:pk>/", views.UpdateMailing.as_view(), name="update_mailing"),
    path("delete_mailing/<int:pk>/", views.DeleteMailing.as_view(), name="delete_mailing"),

    path("sending_messages/<int:pk>/", views.SendingMessages.as_view(), name="sending_messages"),
    path("create_sending_messages/<int:pk>/", views.CreateSendingMessages.as_view(), name="create_sending_messages"),
    path("mailing_statistics/", views.MailingStatistics.as_view(), name="mailing_statistics"),
]
