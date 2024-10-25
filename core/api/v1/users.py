from rest_framework import  generics
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from core.serializers.users import LoginSerializer, UserSerializer
from core.utils.messages import APIResponse
from core.utils.validate import validate_serializer
from rest_framework.schemas import AutoSchema
from core.injector.injector import BaseInjector
from core.repositories.user_repo import UserRepo
from django.contrib.auth import authenticate

class CommonUserView(APIView , AutoSchema):
    user_repo = BaseInjector.get(UserRepo)

class Login(CommonUserView,generics.GenericAPIView):
    serializer_class = LoginSerializer
    @validate_serializer()
    def post(self, request):
        try:
            user = authenticate(username =request.data.get('username') , password = request.data.get('password'))

            if user : 
                refresh = RefreshToken.for_user(user)
                return APIResponse(
                    data={'refresh': str(refresh),
                        'access': str(refresh.access_token)},
                    status=200)
            
            return APIResponse(status=401 , error_code= 1000)
        except Exception as e:

            # capture exception with a tool like sentry
            return APIResponse(status=400 , error_code= 1011 , data = str(e))
        

class Register(CommonUserView,generics.GenericAPIView):
    serializer_class = UserSerializer
    @validate_serializer()
    def post(self, request):
        try :
            user = self.user_repo.create_user(request.data)
            if user : 
                return APIResponse(
                    data=self.get_serializer(user).data,
                    status = 201
                )
            return APIResponse(status=401 , error_code= 1012)
        except Exception as e:
            # capture exception with a tool like sentry
            return APIResponse(status=400 , error_code= 1011 , data = str(e))