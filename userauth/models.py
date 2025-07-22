from django.contrib.auth.models import AbstractUser
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import post_save




# def user_directory_path(instance,filename):
#     ext=filename.split('.')[-1]
#     filename= "%s.%s" % (instance.user.id,filename)
#     return "user_{0}/{1}".format(instance.user.id,filename)


def user_directory_path(instance, filename):
    return f"user_{instance.user.id}/{filename}"


Gender = (
    ("Female", "Female"),
    ("Male", "Male"),
)

IDENTITY_TYPE = (
    ("National Identication Number", "National Identity Number"),
    ("Driver's Licence", "Driver's Licence"),
    ("International Passport", "International Passport"),
)


class User(AbstractUser):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=Gender, default="Male")

    opt = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return str(self.username)


class Profile(models.Model):
    pid = ShortUUIDField(
        length=7, max_length=25, alphabet="abcdefjhigklmnopqrstuvwxwz123456"
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to=user_directory_path, default="default.jpg",null=True,blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=Gender, default="Male")

    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)

    identity_type = models.CharField(
        max_length=100, choices=IDENTITY_TYPE, null=True, blank=True
    )
    
    identity_image=models.FileField(upload_to=user_directory_path, default="id.jpg" ,null=True,blank=True)

    facebook=models.URLField(null=True,blank=True)
    twitter=models.URLField(null=True,blank=True)
    
    wallet=models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    verified=models.BooleanField(default=False)

    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-date']

    

    def __str__(self):
        if self.full_name:
            return f"{self.full_name}"
        else:
            return f"{self.user.username}"
        
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()

post_save.connect(create_user_profile,sender=User)
post_save.connect(save_user_profile,sender=User)



    
