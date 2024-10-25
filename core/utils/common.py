from rest_framework.exceptions import ErrorDetail
from rest_framework.views import APIView
from core.utils.messages import APIResponse


class ValidateAndHandleErrors(APIView):

    @staticmethod
    def validate_and_handle_errors(serializer):
        serializer.is_valid()
        if serializer.errors:
            for key, value in serializer.errors.items():
                if isinstance(value, list):
                    for error_detail in value:
                        if isinstance(error_detail, ErrorDetail):
                            if error_detail.code == 'blank':
                                return APIResponse(data="", error_code=1004, status=404)
                            if error_detail.code == 'max_length':
                                return APIResponse(data="", error_code=1006, status=404)
                            if error_detail.code == 'required':
                                return APIResponse(data="", error_code=1004, status=404)
                            if error_detail.code == 'invalid':
                                return APIResponse(data="", error_code=1000, status=404)
                            if error_detail.code == 'unique':
                                return APIResponse(data="", error_code=1007, status=404)
                            if error_detail.code == 'password_mismatch':
                                return APIResponse(data="", error_code=1008, status=404)
                            if error_detail.code == 'invalid_choice':
                                return APIResponse(data="", error_code=1009, status=404)
                            if error_detail.code == 'min_length':
                                return APIResponse(data="", error_code=1010, status=404)
                            if error_detail.code == 'max_value':
                                return APIResponse(data="", error_code=1006, status=404)
                            if error_detail.code == 'min_value':
                                return APIResponse(data="", error_code=1010, status=404)
                            
                return APIResponse(data="", error_code=1011, status=500)

        return None
