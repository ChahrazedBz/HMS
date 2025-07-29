from django.urls import path

from . import views

app_name = "booking"

urlpatterns = [
    path(
        "check_room_available/", views.check_room_available, name="check_room_available"
    )
    
]
