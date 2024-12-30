from django.contrib import admin
from properties.models import Property,PropertyImage,PropertyType

admin.site.register(Property)
admin.site.register(PropertyType)
admin.site.register(PropertyImage)
