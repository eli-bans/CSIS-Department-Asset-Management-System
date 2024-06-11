# users/urls.py

from django.urls import path
from .views import RegisterView, LoginView, MagicLinkLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('magic-link-login/', MagicLinkLoginView.as_view(), name='magic_link_login'),
]
