from django.urls import path
from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("login/", views.MyLogin.as_view(), name="login"),
    path("logout/", views.MyLogout.as_view(), name="logout"),
    path("register/", views.CreateUser.as_view(), name="register"),
    path("email-confirm/<str:token>/", views.email_verification, name="email-confirm"),
    path("verification/", views.Verification.as_view(), name="verification"),
    path("change_profile/<int:pk>/", views.UpdateUser.as_view(), name="change_profile"),
    path("change_profile/password/", views.PasswordsChangeUser.as_view()),
    path("detail_user/", views.DetailUser.as_view(), name="detail_user"),
    path("list_users/", views.ListUsers.as_view(), name="list_users"),
    path("user_information/<int:pk>/", views.DetailUserOfService.as_view(), name="user_information"),
]

