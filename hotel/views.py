from datetime import datetime
from decimal import Decimal
import stripe
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
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
    Notification
)


def index(request):
    hotels = Hotel.objects.filter(status="Live")

    context = {"hotels": hotels}

    return render(request, "hotel/index.html", context)


def hotel_detail(request, slug):
    hotel = Hotel.objects.get(status="Live", slug=slug)
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
    rooms = Room.objects.filter(room_type=room_type, is_available=True)

    id = request.GET.get("hotel-id")
    checkin = request.GET.get("checkin")
    checkout = request.GET.get("checkout")
    adult = request.GET.get("adult")
    children = request.GET.get("children")

    context = {
        "hotel": hotel,
        "room_type": room_type,
        "rooms": rooms,
        "id": id,
        "checkin": checkin,
        "checkout": checkout,
        "adult": adult,
        "children": children,
    }
    return render(request, "hotel/room_type_detail.html", context)


def selected_rooms(request):
    total = 0
    room_count = 0
    total_days = 0
    adult = 0
    children = 0
    checkin = ""
    checkout = ""

    if "selection_data_obj" in request.session:

        if request.method == "POST":
            for h_id, item in request.session["selection_data_obj"].items():
                id = int(item["hotel_id"])
                checkin = item["checkin"]
                checkout = item["checkout"]
                adult = int(item["adult"])
                children = int(item["children"])
                room_type = int(item["room_type"])
                room_id = int(item["room_id"])

                user = request.user
                hotel = Hotel.objects.get(id=id)
                room_type = RoomType.objects.get(id=room_type)
                room = Room.objects.get(id=room_id)

            date_format = "%Y-%m-%d"
            checkin_date = datetime.strptime(checkin, date_format)
            checkout_date = datetime.strptime(checkout, date_format)
            time_defference = checkout_date - checkin_date
            total_days = time_defference.days

            full_name = request.POST.get("full_name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")

            booking = Booking.objects.create(
                hotel=hotel,
                room_type=room_type,
                check_in_date=checkin,
                check_out_date=checkout,
                total_days=total_days,
                num_adults=adult,
                num_children=children,
                full_name=full_name,
                email=email,
                phone=phone,
                user=request.user or None,
            )
            for h_id, item in request.session["selection_data_obj"].items():
                room_id = int(item["room_id"])
                room = Room.objects.get(id=room_id)
                booking.room.add(room)

                room_count += 1
                days = total_days
                price = room_type.price

                room_price = price * room_count
                total = room_price * days

            booking.total += float(total)
            booking.before_discount += float(total)
            booking.save()

            return redirect("hotel:checkout", booking.booking_id)

        hotel = None
        for h_id, item in request.session["selection_data_obj"].items():
            id = int(item["hotel_id"])
            checkin = item["checkin"]
            checkout = item["checkout"]
            adult = int(item["adult"])
            children = int(item["children"])
            room_type = int(item["room_type"])
            room_id = int(item["room_id"])

            room_type = RoomType.objects.get(id=room_type)

            date_format = "%Y-%m-%d"
            if checkin and checkout:
                checkin_date = datetime.strptime(checkin, date_format)
                checkout_date = datetime.strptime(checkout, date_format)
                time_defference = checkout_date - checkin_date
                total_days = time_defference.days
            else:
                messages.error(request, "Missing check-in or check-out date.")
                return redirect("/")

            room_count += 1
            days = total_days
            price = room_type.price

            room_price = price * room_count
            total = room_price * days
            hotel = Hotel.objects.get(id=id)
        context = {
            "data": request.session["selection_data_obj"],
            "total_selected_items": len(request.session["selection_data_obj"]),
            "checkin": checkin,
            "checkout": checkout,
            "adult": adult,
            "children": children,
            "room_type": room_type,
            "room_id": room_id,
            "total_days": total_days,
            "total": total,
            "hotel": hotel,
        }
        return render(request, "hotel/selected_rooms.html", context)

    else:
        messages.warning(request, "No rooms has been selected yet")
        return redirect("/")


def checkout(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)
    if request.method == "POST":
        code = request.POST.get("code")
        try:
            coupon = Coupon.objects.get(code__iexact=code, active=True)
            if coupon in booking.coupons.all():
                messages.warning(request, "coupon already activated")
                return redirect("hotel:checkout", booking.booking_id)
            else:
                if coupon.type == "Percentage":
                    discount = booking.total * coupon.discount / 100
                else:
                    discount = coupon.discount

                booking.coupons.add(coupon)
                booking.total -= discount
                booking.saved += discount
                booking.save()

                messages.success(request, "coupon  activated")
                return redirect("hotel:checkout", booking.booking_id)
        except:
            messages.error(request, "coupon  doesnt exist")
            return redirect("hotel:checkout", booking.booking_id)
    context = {"booking": booking, "stripe_publishable_key": settings.STRIPE_PUBLIC_KEY}

    return render(request, "hotel/checkout.html", context)


@csrf_exempt
def create_checkout_session(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        customer_email=booking.email,
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "USD",
                    "product_data": {"name": booking.full_name},
                    "unit_amount": int(booking.total * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse("hotel:success", args=[booking.booking_id])
        )
        + "?session_id={CHECKOUT_SESSION_ID}&success_id="
        + booking.success_id
        + "&booking_total"
        + str(booking.total),
        cancel_url=request.build_absolute_uri(
            reverse("hotel:failed", args=[booking.booking_id])
        ),
    )
    booking.payment_status = "Processing"
    booking.stripe_payment_intent = checkout_session["id"]
    booking.save()

    print("checkout session", checkout_session)
    return JsonResponse({"sessionId": checkout_session.id})


def payment_success(request, booking_id):
    success_id=request.GET.get('success_id')
    booking_total=request.GET.get('booking_total')

    if success_id and booking_total :
        success_id=success_id.rstripe("/")
        booking_total=booking_total.rstripe("/")

        booking=Booking.objects.get(booking_id=booking_id,success_id=success_id)
        if booking.total==Decimal(booking_total):
            print("Booking total matched")
            if booking.payment_status =='Processing':
                booking.payment_status ='Paid'
                booking.save()

                noti=Notification.objects.create(
                    booking=booking,
                    type="Booking Confirmed",
                )
                if request.user.is_authenticated:
                    noti.user=request.user
                else:
                    noti.user=None

                noti.save()

                if 'selection_data_obj' in request.session:
                    del request.session['selection_data_obj']
            else:
                messages.success(request,"Payment made already ,Thanks for your patronage")

        else:
            print("Error : Payment manipulation detected")


    context={
        'booking':booking
    }

    return render(request,"hotel/payment_success.html",context)


def payment_failed(request, booking_id):
    return render(request,"hotel/payment_failed.html")

    
