from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/Encyclopedia:Create_Page", views.create, name="create"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("random", views.randompage, name="random"),
    path("edit", views.edit, name="edit")
]
