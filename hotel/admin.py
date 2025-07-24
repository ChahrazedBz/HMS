from django.contrib import admin

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

class HotelGalleryInline(admin.TabularInline):
    model = HotelGallery

class HotelFeaturesInline(admin.TabularInline):
    model=HotelFeatures

class RoomTypeInline(admin.TabularInline):
    model=RoomType

    
class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelGalleryInline,HotelFeaturesInline,RoomTypeInline]
    list_display = ["thumbnail", "name", "user", "status"]
    prepopulated_fields = {"slug": ("name",)}


class HotelGAdmin(admin.ModelAdmin):
    list_display = ["hgid", "hotel"]





class HotelFtrsAdmin(admin.ModelAdmin):
    list_display = ["hotel", "name", "icon"]


class HotelFaqsAdmin(admin.ModelAdmin):
    list_display = ["question", "answer", "date"]


class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ["type", "number_of_beds", "room_capacity", "price"]


class RoomAdmin(admin.ModelAdmin):
    list_display = ["room_number", "room_type", "is_available"]


class BookingAdmin(admin.ModelAdmin):
    list_display = ["hotel", "user", "room_type", "total_days", "total"]


class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ["booking", "date"]


class StaffOnDutyAdmin(admin.ModelAdmin):
    list_display = ["booking", "staff_id", "date"]


class CouponAdmin(admin.ModelAdmin):
    list_display = ["type", "code", "discount", "redemptions", "active"]


admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelGallery, HotelGAdmin)
admin.site.register(HotelFeatures, HotelFtrsAdmin)
admin.site.register(HotelFaqs, HotelFaqsAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(ActivityLog, ActivityLogAdmin)
admin.site.register(StaffOnDuty, StaffOnDutyAdmin)
admin.site.register(Coupon, CouponAdmin)
