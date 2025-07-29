from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
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


def check_room_available(request):
    if request.method =='POST':
        id=request.POST.get("hotel-id")
        checkin=request.POST.get("checkin")
        checkout=request.POST.get("checkout")
        adult=request.POST.get("adult")
        children=request.POST.get("children")
        room_type=request.POST.get("room_type")
        
        print("id===========",id)
        print("id===========",checkin)
        print("id===========",checkout)
        print("id===========",adult)
        print("id===========",children)
        print("id===========",room_type)
        
        hotel=Hotel.objects.get(id=id)
        room_type=RoomType.objects.get(slug=room_type,hotel=hotel)

        url=reverse("hotel:room_type_detail",args=[hotel.slug,room_type.slug])
        url_with_params=f"{url}?hotel-id={id}&checkin={checkin}&checkout={checkout}&adult={adult}&children={children}&room-type={room_type}"

    return HttpResponseRedirect(url_with_params)
   