import jwt # type:ignore
from tenant.serializers import*
from Rentwalain.settings import SECRET_KEY
from tenant.models import TenantProfile
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed,ValidationError


def Authentication(request):
    token = request.headers.get('App-AUTH')
    if token:
        split_value = token.split(' ')
        if len(split_value) == 2 and split_value[0] == "SJWT":
            try:
                decoded = jwt.decode(split_value[1], SECRET_KEY, algorithms=["HS256"])
                user = TenantProfile.objects.filter(id = decoded.get('id')).first()
                if user:
                    return decoded
                else:
                    raise ValidationError('User not found')
            except Exception as e:
                raise AuthenticationFailed
        raise ValidationError('Invalid Credentials')
    raise AuthenticationFailed

class IsTenant(BasePermission):
    def has_permission(self, request, view):
        data = Authentication(request)
        if  data.get('type') == 'T':
            request.user_id = data.get('id')
            return True
        else:
            return False