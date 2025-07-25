from django.shortcuts import render

from hotel.models import (
    ActivityLog,
    Booking,
    Coupon,
    Hotel,
    HotelFaqs,
    HotelFeatures,
    HotelGallery,
    Room,
    RoomType,
    StaffOnDuty,
)


def index(request):
    hotels = Hotel.objects.filter(status="Live")

    context = {"hotels": hotels}

    return render(request, "hotel/index.html", context)


def hotel_detail(request, slug):
    hotel = Hotel.objects.get(status="Live",slug=slug)
    features = hotel.hotel_features()
    half = len(features) // 2 + len(features) % 2
    left_features = features[:half]
    right_features = features[half:]
   
    context = {
        "hotel": hotel,
        "left_features": left_features,
        "right_features": right_features,
    }
    return render(request, "hotel/hotel_detail.html", context)


def room_type_detail(request, slug, rt_slug):
    hotel = Hotel.objects.get(status="Live", slug=slug)
    room_type = RoomType.objects.get(hotel=hotel, slug=rt_slug)
    rooms = Room.objects.filter( room_type=room_type,is_available=True)

    context = {"hotel": hotel, "room_type": room_type, "rooms": rooms}
    return render(request, "hotel/room_type_detail.html", context)
