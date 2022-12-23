import jwt
import traceback
from django.conf import settings
from applications.users.models.systemuser import SystemUser

class TokenSimpleJWTAuth:
    def get_user_id_from_token(token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return payload['user_id']
        except:
            tb = traceback.format_exc()
            print(tb)
            return 'error decoding token'

    def get_type_systemuser_from_auth_id( id ):
        try:
            systemuser = SystemUser.objects.get( auth_user = id)
            return systemuser.type
        except:
            return None