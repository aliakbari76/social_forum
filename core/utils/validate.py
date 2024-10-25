from functools import wraps
from core.utils.common import ValidateAndHandleErrors


def validate_serializer():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            result = ValidateAndHandleErrors.validate_and_handle_errors(serializer)
            if result:
                #print('serializer error ' +  str(result))
                return result
            return view_func(self, request, *args, **kwargs)

        return wrapper

    return decorator
