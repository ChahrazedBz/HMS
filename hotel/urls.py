from django.urls import path

from . import views

app_name = "hotel"

urlpatterns = [
    path("", views.index, name="index"),
    path("detail/<slug>", views.hotel_detail, name="hotel_detail"),
    path(
        "detail/<slug:slug>/room-type/<slug:rt_slug>",
        views.room_type_detail,
        name="room_type_detail",
    ),
]
