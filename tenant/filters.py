import django_filters # type: ignore
from properties.models import Property

class PropertyFilter(django_filters.FilterSet):
    
    class Meta:
        model = Property
        fields = {
            'property_type' : ['exact'],
            'price_per_month' : ['gte','lte'],
            'num_of_bedrooms' : ['gte','lte'],
            'num_of_bathrooms' : ['gte','lte'],
            'available_from' :['exact']
        }