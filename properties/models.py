import os
from django.db.models.signals import post_delete
from django.db import models
from django.dispatch import receiver
from landlord.models import LandlordProfile


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class PropertyType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Property(BaseModel):
    landlord = models.ForeignKey(LandlordProfile, on_delete=models.CASCADE, related_name='properties')
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    num_of_bedrooms = models.PositiveIntegerField()
    num_of_bathrooms = models.PositiveIntegerField()
    available_from = models.DateField()

    def __str__(self):
        return f"{self.landlord} - {self.title} "


class PropertyImage(models.Model):
    property  = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE, null=True,blank=True)
    image = models.ImageField(upload_to='images/',null=True,blank=True)
    def __str__(self):
        return f"Owner {self.property.landlord} Image for {self.property.title}"
    class Meta:
        ordering = ['-id']



@receiver(post_delete, sender=Property)
def delete_property_images(sender, instance, **kwargs):
    for image in instance.images.all():
        if image.image:
            if os.path.isfile(image.image.path):
                os.remove(image.image.path)
                
@receiver(post_delete, sender=PropertyImage)
def delete_individual_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)