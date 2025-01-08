import json
from Rentwalain.settings import BASEURL
import requests # type: ignore
from django.contrib import messages
from rest_framework.views import APIView
from properties.models import PropertyType
from django.shortcuts import render,redirect
from rest_framework.response import Response
from landlord.authentication import IsLandlord
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 10

class HomeView(APIView):
    pagination_class = StandardResultsSetPagination
    
    def get(self, request):
        property_type = request.GET.get('property_type')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        num_of_bedrooms = request.GET.get('num_of_bedrooms')
        num_of_bathrooms = request.GET.get('num_of_bathrooms')
        available_from = request.GET.get('available_from')
        city = request.GET.get('city')

        params = {}
        if property_type:
            params['property_type'] = property_type
        if min_price:
            params['price_per_month__gte'] = min_price
        if max_price:
            params['price_per_month__lte'] = max_price
        if num_of_bedrooms:
            params['num_of_bedrooms__gte'] = num_of_bedrooms
        if num_of_bathrooms:
            params['num_of_bathrooms__gte'] = num_of_bathrooms
        if available_from:
            params['available_from__gte'] = available_from
        if city:
            params['search'] = city

        # Send the GET request with filters to the API
        api_url = BASEURL+"/tenant/home/"
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            properties = response.json()
        else:
            properties = []
        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(properties, request)
        if paginated_data is not None:
            paginated_response = paginator.get_paginated_response(paginated_data)
            context = {
            "count": paginated_response.data.get('count'),
            "next": paginated_response.data.get('next'),
            "previous": paginated_response.data.get('previous'),
            "properties": paginated_response.data.get('results')
            }
        return render(request, 'home.html',context)
    
class DetailsView(APIView):
    def get(self,request,id):
        api_url = BASEURL+f"/tenant/home/{id}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
        return render(request,'details.html',{'property':data})

class ProfileView(APIView):
    def get(self,request):
        token = request.session.get('auth_token')
        user_type = request.session.get('user_type')
        if not token or not user_type:
            return redirect('login')
        
        headers = {'App-AUTH': token}
        
        if user_type == 'landlord':
            profile_url = BASEURL+'/landlord/profile/' 
            property_url = BASEURL+'/property/rentals/' 
        elif user_type == 'tenant':
            profile_url = BASEURL+'/tenant/profile/'
        else:
            return render(request, 'login.html', {'error': 'Invalid user type'})

        if user_type =="landlord":
            response = requests.get(profile_url, headers=headers)
            p_response = requests.get(property_url, headers=headers)
            if response.status_code == 200 and p_response.status_code ==200:
                user_data = response.json()
                property_data = p_response.json()
                return render(request, 'profile.html', {"user": user_data,"properties":property_data})
            else:
                return render(request, 'login.html', {'error': 'Failed to fetch user profile.'})        
        else:    
            response = requests.get(profile_url, headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                return render(request, 'profile.html', {"user": user_data})
            else:
                return render(request, 'login.html', {'error': 'Failed to fetch user profile.'})
        
    def post(self,request,id):
        token = request.session.get('auth_token')
        headers = {'App-AUTH': token}
        form_data = request.POST.copy()
        file={
            'profilepic':request.FILES.get("profilepic")
        }
        form_data['is_active'] = form_data.get('is_active') == 'on'
        user_type = request.session.get('user_type')
        if user_type == 'landlord':
            profile_url = f'{BASEURL}/landlord/profile/{id}/'
        else:
            profile_url = f'{BASEURL}/tenant/profile/{id}'
        response = requests.patch(profile_url, headers=headers, json=form_data ,files=file)
        if response.status_code == 200:
            user_data = response.json()
            return redirect('profile') 
        return render(request,'profile.html')      

class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        usertype = request.POST.get('usertype')
        if usertype == 'landlord':
            api_url = BASEURL+'/landlord/login/'
        elif usertype == 'tenant':
            api_url = BASEURL+'/tenant/login/'
        else:
            return render(request, 'login.html', {'error': 'Invalid user type'})
        response = requests.post(api_url, data={'email': email, 'password': password})
        
        if response.status_code == 200:
            token = response.json().get('token')  
            request.session['auth_token'] = f'SJWT {token}'
            request.session['user_type'] = usertype  
            return redirect('/profile/') 
        else:
            messages.info(request, "Invalid credentials")
            return render(request, 'login.html',{'messages': messages.get_messages(request)})

class RegisterView(APIView):
    def get(self, request):
        return render(request, 'register.html')
    
    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        usertype = request.data.get('usertype')
        if not (first_name and last_name and email and phone_number and password and usertype):
            messages.error(request, "All fields are required.")
            return redirect('register')

        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "password": password,
        }
        if usertype == 'landlord':
            api_url = BASEURL+"/landlord/register/"
        elif usertype == 'tenant':
            api_url = BASEURL+"/tenant/register/"
        else:
            messages.error(request, "Invalid user type.")
            return redirect('register')
        try:
            response = requests.post(api_url, json=payload) 
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Failed to connect to the server: {e}")
            return redirect('register')
        if response.status_code == 201:  
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        else:
            error_message = response.json().get('detail', response.text)
            error_message= json.loads(error_message).get("email", [None])[0]
            messages.error(request, error_message)
            return redirect('register')
            
class LogoutView(APIView):
    def get(self,request):
        if 'auth_token' in request.session:
            del request.session['auth_token']
            del request.session['user_type']
        messages.success(request, "Logged out successfully")
        return redirect('/login/')
        
class AddPropertyView(APIView):
    def get(self,request):
        if request.session.get('user_type') == 'landlord' and request.session.get('auth_token'):
            property_types = PropertyType.objects.all()
            return render(request, 'property.html', {'property_types': property_types})
        else:
            return redirect('login')
    def post(self, request, *args, **kwargs):
        token = request.session.get('auth_token')
        headers = {'App-AUTH': token}
        data=request.data
        data.pop('images')
        images = request.FILES.get('images')  

        # Prepare the 'files' dictionary for the request
        files = {}
        if images:
            files['images'] = images  # 'images' should match the serializer field name

        api_url = BASEURL+'/property/rentals/'

        # Send the POST request to the API
        response = requests.post(api_url, headers=headers, data=data, files=files)

        # Handle the response
        if response.status_code == 201:
            property_data = response.json()
            messages.success(request,"Property added successfully")
            return redirect('addProperty')
        else:
            return render(request, 'property.html', {"error": "Failed to add property."})
        
class ViewEditProperty(APIView):
    def get(self,request,id):
        api_url = BASEURL+f'/property/rentals/{id}/'
        token = request.session.get('auth_token')
        headers = {'App-AUTH': token}
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            property_data = response.json()
            return render(request,'view.html',{'property':property_data})
        else:
            return redirect('login')
    def post(self,request,id):
        data = request.POST.copy()
        data['is_active'] = data.get('is_active') == 'on'
        return redirect('profile')

class DeleteProperty(APIView):
    def get(self,request,id):
        api_url = BASEURL+f'/property/rentals/{id}/'
        token = request.session.get('auth_token')
        headers = {'App-AUTH': token}
        response = requests.delete(api_url, headers=headers)
        messages.success(request,"Property deleted")
        return redirect('profile')
        
class EditImageView(APIView):
    def post(self, request, id):
        api_url = BASEURL + f'/property/propertyImages/'
        token = request.session.get('auth_token')
        if not token:
            messages.error(request, "Authentication token is missing.")
            return redirect('profile')

        headers = {'App-AUTH': token}
        data = {"property": id}
        file = {'image': request.FILES.get('image')}
        
        response = requests.post(api_url, headers=headers, data=data, files=file)
        if response.status_code == 201:
            messages.success(request, "Image added successfully")
        else:
            messages.error(request, "Failed to add image!")
        return redirect('profile')
    def get(self,request,id):
        api_url = BASEURL+f'/property/propertyImages/{id}/'
        token = request.session.get('auth_token')
        headers = {'App-AUTH': token}
        response = requests.delete(api_url, headers=headers)
        messages.success(request,"Image deleted")
        return redirect('profile')