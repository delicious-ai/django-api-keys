from django.urls import path

from . import views

urlpatterns = [
    path(
        "fruits",
        views.get_fruits,
    ),
]
