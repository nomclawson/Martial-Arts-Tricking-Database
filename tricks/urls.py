from django.urls import path
from . import views

urlpatterns = [
    path("", views.sign_in, name="sign_in"),
    path("index_user", views.index_user, name="index_user"),
    path("index_all", views.index_all, name="index_all"),
    path("<int:pk>/", views.detail, name="detail"),
]