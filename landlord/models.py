from django.db import models

class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
        
class LandlordProfile(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    profilepic = models.ImageField(upload_to="profiles/",default="profiles/unnamed.webp",null=True,blank=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
