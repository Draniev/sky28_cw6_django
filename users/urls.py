from django.urls import path

from users.apps import UsersConfig
from users.views import CustomLoginView, CustomSignupView, ActivateAccountView, CustomLogoutView

app_name = UsersConfig.name

urlpatterns = [
    path('', CustomLoginView.as_view(), name='sign-in'),
    path('sign-up/', CustomSignupView.as_view(), name='sign-up'),
    path('activate/', ActivateAccountView.as_view(), name='activate'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
