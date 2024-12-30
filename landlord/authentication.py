from .models import LandlordProfile
from landlord.serializers import*
import jwt # type: ignore
from Rentwalain.settings import SECRET_KEY
from rest_framework.exceptions import AuthenticationFailed,ValidationError
from rest_framework.permissions import BasePermission

def Authentication(request):
    token = request.headers.get('App-AUTH')
    if token:
        split_value = token.split(' ')
        if len(split_value) == 2 and split_value[0] == 'SJWT':
            try:
                decoded = jwt.decode(split_value[1], SECRET_KEY, algorithms=["HS256"])
                user = LandlordProfile.objects.filter(id=decoded.get('id')).first()
                if user:
                    return decoded
                else:
                    raise ValidationError('user not found')
            except Exception as e:
                print('error',e)
                raise AuthenticationFailed
                
        else:
            raise AuthenticationFailed
    else:
        raise AuthenticationFailed
    
class IsLandlord(BasePermission):
    def has_permission(self, request, view):
        data = Authentication(request)
        if  data.get('type') == 'L':
            request.user_id = data.get('id')
            return True
        else:
            return False