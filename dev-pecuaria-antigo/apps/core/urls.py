from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import *

urlpatterns = [
    path("", login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("home/", home, name="home"),
    path("admin/", admin.site.urls),
    path("pecuaria/", include("apps.pecuaria.urls"), name='pecuaria'),
    path("feedback/", include("apps.feedback.urls"), name='feedback'),
    path("edificios/", include("apps.edificios.urls"), name='edificios'),
    path("seguranca/", include("apps.seguranca.urls"), name='seguranca'),
    path("industria/", include("apps.industria.urls"), name='industria'),
]
