from django.db import models
from userauth.models import User
from shortuuid.django_fields import ShortUUIDField
import shortuuid
from django.utils.text import slugify 
from django.utils.html import mark_safe

HOTEL_STATUS=(
    ('Draft','Draft'),
    ('Diseabled','Diseabled'),
    ('Rejected','Rejected'),
    ('In Review','In Review'),
    ('Live','Live'),
)


class Hotel(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL ,null=True)
    name=models.CharField(max_length=200)
    description=models.CharField(max_length=300)
    image=models.FileField(upload_to='Hotel_gallery')
    address=models.CharField(max_length=200)
    email=models.EmailField(unique=True,max_length=100)
    mobile=models.CharField(max_length=100)

    tags=models.CharField(max_length=20,help_text='seperate tags with comma')
    views=models.PositiveIntegerField(default=0)
    featured=models.BooleanField(default=False)
    
    hid=ShortUUIDField(unique=True,length=10 ,max_length=20,alphabet='abxchdjkiryteqolp')
    slug=models.SlugField(unique=True)


    status=models.CharField(max_length=20,choices=HOTEL_STATUS,default='Live')

    def __str__(self):
        return str(self.name)
    
    def save(self,*args,**kwargs):
        if self.slug =='' or self.slug ==None:
            uuid_key=shortuuid.uuid()
            unique_id=uuid_key[:4]
            self.slug=slugify(self.name)+ '-'+str(unique_id.lower())
        super(Hotel,self).save(*args,**kwargs)

    def thumbnail(self):
        return mark_safe(
            "<img src='%s' width='50' height='50' style='object-fit: cover; border-radius: 6px;' />" % self.image.url
        )

    


