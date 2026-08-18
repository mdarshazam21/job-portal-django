from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.login_view, name="logout"),
    path('company/create/', views.company_profile_create, name='company_profile_create'),
]
