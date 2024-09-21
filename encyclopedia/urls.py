from django.urls import path
from . import views
from django.views.generic.base import RedirectView

app_name = "encyclopedia"  # Zorg dat dit bovenaan staat om een namespace te registreren

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.page, name="page"),  # Zorg dat deze URL correct overeenkomt met de reverse functie in je view
    path("searchresults/<str:title>", views.searchresults, name="searchresults"),
    path("create", views.create, name="create"),
    path("edit/<str:title>", views.edit, name="edit"),
]

