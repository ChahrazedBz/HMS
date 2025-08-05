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
    path("selected_rooms/", views.selected_rooms, name="selected_rooms"),
    path("checkout/<str:booking_id>/", views.checkout, name="checkout"),
    # Payment Routes
    path(
        "api/create_checkout_session/<str:booking_id>/",
        views.create_checkout_session,
        name="api_checkout_session",
    ),
    path("success/<str:booking_id>/", views.payment_success, name="success"),
    path("failed/<str:booking_id>/", views.payment_failed, name="failed"),
]
