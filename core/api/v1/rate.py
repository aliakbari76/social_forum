from rest_framework import status , generics
from rest_framework.views import APIView
from core.utils.messages import APIResponse
from core.utils.validate import validate_serializer
from rest_framework.schemas import AutoSchema
from core.injector.injector import BaseInjector
from rest_framework_simplejwt.authentication import JWTAuthentication
from core.repositories.rate_repo import RateRepo
from core.schemas.rate_schema import RateSchema
from core.services.redis_services import RedisService
from core.serializers import RateSerializer
class CommonRateView(AutoSchema , APIView):
    rate_repo = BaseInjector.get(RateRepo)
    redis_service = BaseInjector.get(RedisService)


class RatePostView(CommonRateView , generics.CreateAPIView):
    serializer_class = RateSerializer
    authentication_classes = [JWTAuthentication]
    @validate_serializer()
    def post(self , request):
        try:
            is_done = self.rate_repo.create_or_update_rate(RateSchema(rate = request.data.get('rate') , post_id = request.data.get('post_id') , user_id = request.user.id))
            if is_done:
                return APIResponse(status = 201, success= 2002)
            return APIResponse(status=417 , error_code= 1000)
        except Exception as e:
            #capture exception with a tool like sentry
            return APIResponse(status=400 , error_code= 1011 , data = str(e))