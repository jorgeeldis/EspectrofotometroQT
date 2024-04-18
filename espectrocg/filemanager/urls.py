from django.urls import path
from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("upload", views.subir_documento, name="subir_documento"),
  path("about", views.about, name="about"),
]