from django.urls import path

from . import views

app_name = "booking"

urlpatterns = [
    path(
        "check_room_available/", views.check_room_available, name="check_room_available"
    ),
    path(
        "add_room_selection/", views.add_room_selection, name="add_room_selection"
    )
    
]
