import shortuuid
from django.db import models
from django.utils.html import mark_safe
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from shortuuid.django_fields import ShortUUIDField
from taggit.managers import TaggableManager

from userauth.models import User

HOTEL_STATUS = (
    ("Draft", "Draft"),
    ("Diseabled", "Diseabled"),
    ("Rejected", "Rejected"),
    ("In Review", "In Review"),
    ("Live", "Live"),
)

ICON_TYPE = (
    ("Bootstrap Icons", "Bootstrap Icons"),
    ("Fontawsome Icons", "Fontawsome Icons"),
    ("Box Icons", "Box Icons"),
    ("Remi Icons", "Remi Icons"),
    ("Flat Icons", "Flat Icons"),
)


PAYMENT_STATUS = (
    ("Paid", "Paid"),
    ("Pending", "Pending"),
    ("Processing", "Processing"),
    ("cancelled", "cancelled"),
    ("initiated", "initiated"),
    ("failed", "failed"),
    ("refunding", "refunding"),
    ("refunded", "refunded"),
    ("unpaid", "unpaid"),
    ("expired", "expired"),
)


class Hotel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = CKEditor5Field(null=True, blank=True, config_name="default")
    image = models.FileField(upload_to="Hotel_gallery")
    address = models.CharField(max_length=200)
    email = models.EmailField(unique=True, max_length=100)
    mobile = models.CharField(max_length=100)

    tags = TaggableManager(blank=True)
    views = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    facebook = models.URLField(max_length=100, default="https://facebook.com")
    instagram = models.URLField(max_length=100, default="https://facebook.com")
    twitter = models.URLField(max_length=100, default="https://facebook.com")

    hid = ShortUUIDField(
        unique=True, length=10, max_length=20, alphabet="abxchdjkiryteqolp"
    )
    slug = models.SlugField(unique=True)

    status = models.CharField(max_length=20, choices=HOTEL_STATUS, default="Live")

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            uuid_key = shortuuid.uuid()
            unique_id = uuid_key[:4]
            self.slug = slugify(self.name) + "-" + str(unique_id.lower())
        super(Hotel, self).save(*args, **kwargs)

    def thumbnail(self):
        return mark_safe(
            "<img src='%s' width='50' height='50' style='object-fit: cover; border-radius: 6px;' />"
            % self.image.url
        )

    def hotel_gallery(self):
        return HotelGallery.objects.filter(hotel=self)

    def hotel_features(self):
        return HotelFeatures.objects.filter(hotel=self)

    def room_type(self):
        return RoomType.objects.filter(hotel=self)

    def rooms(self):
        return Room.objects.filter(hotel=self)


class HotelGallery(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    image = models.FileField(upload_to="Hotel_gallery")
    hgid = ShortUUIDField(
        unique=True, length=10, max_length=20, alphabet="abxchdjkiryteqolp"
    )

    def __str__(self):
        return str(self.hotel.name)

    class Meta:
        verbose_name_plural = "Hotel Gallery"


class HotelFeatures(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    icon_type = models.CharField(
        max_length=200, null=True, blank=True, choices=ICON_TYPE
    )
    icon = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Hotel Features"


class HotelFaqs(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.question)

    class Meta:
        verbose_name_plural = "Hotel FAQs"


class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    image = models.ImageField(upload_to="rooms_type", null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    number_of_beds = models.PositiveIntegerField(default=0)
    room_capacity = models.PositiveIntegerField(default=0)
    rtid = ShortUUIDField(
        unique=True, length=10, max_length=20, alphabet="abxchdjkiryteqolp"
    )
    description = CKEditor5Field(null=True, blank=True, config_name="default")
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.hotel.name} - {self.price}"

    class Meta:
        verbose_name_plural = "Room Types"

    def room_count(self):
        Room.objects.filter(room_type=self).count()

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            uuid_key = shortuuid.uuid()
            unique_id = uuid_key[:4]
            self.slug = slugify(self.name) + "-" + str(unique_id.lower())
        super(RoomType, self).save(*args, **kwargs)


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=100)
    floor = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)
    rid = ShortUUIDField(
        unique=True, length=10, max_length=20, alphabet="abxchdjkiryteqolp"
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room_type.type}  - {self.hotel.name}  -{self.price}"

    class Meta:
        verbose_name_plural = "Rooms"

    @property
    def price(self):
        return self.room_type.price

    def number_of_beds(self):
        return self.room_type.number_of_beds


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS)

    full_name = models.CharField(max_length=1000)
    email = models.EmailField(max_length=1000)
    phone = models.CharField(max_length=100)

    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    room_type = models.ForeignKey(
        RoomType, on_delete=models.SET_NULL, null=True, blank=True
    )
    coupons = models.ManyToManyField("hotel.coupon", blank=True)
    room = models.ManyToManyField(Room)
    before_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    saved = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    check_in_date = models.DateField()
    check_out_date = models.DateField()

    total_days = models.PositiveIntegerField(default=0)
    num_adults = models.PositiveIntegerField(default=1)
    num_children = models.PositiveIntegerField(default=0)

    checked_in = models.BooleanField(default=False)
    checked_out = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)

    checked_in_tracker = models.BooleanField(default=False)
    check_out_tracker = models.BooleanField(default=False)

    booking_id = ShortUUIDField(
        unique=True, length=10, max_length=20, alphabet="abxchdjkiryteqolp"
    )
    date = models.DateTimeField(auto_now_add=True)
    stripe_payment_intent = models.CharField(max_length=1000, null=True, blank=True)
    success_id = ShortUUIDField(
        length=10,
        max_length=20,
        alphabet="abxchdjkiryteqolp",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.booking_id}"

    def rooms(self):
        return self.room.all().count()


class ActivityLog(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    guess_in = models.DateTimeField()
    guess_out = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking}"


class StaffOnDuty(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff_id}"


class Coupon(models.Model):
    code = models.CharField(max_length=1000)
    type = models.CharField(max_length=100, default="Percentage")
    discount = models.IntegerField(default=1)
    redemptions = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    cid = ShortUUIDField(
        unique=True, length=10, max_length=20, alphabet="abxchdjkiryteqolp"
    )

    def __str__(self):
        return f"{self.code}"
