from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/Encyclopedia:Search",views.search, name='search'),
    path("wiki/<str:title>", views.entry, name='entry'),
    path("random", views.randompage, name="random")
]
