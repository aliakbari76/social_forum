from django.http import JsonResponse


class APIResponse(JsonResponse):
    def __init__(self, data=None, error_code=None, status=None, success=None , content_type='application/json'):
        content = {'error': {}, 'data': data}
        if error_code:
            content['error'] = {'code': error_code, 'description': ErrorMessage.errors[error_code]}
        if success :
            content["data"] = {'code':success ,  'description':SuccessMessage.Success[success]}
            if data:
                content["data"]["object"] = data
                
        super().__init__(content, status=status, content_type=content_type)
        


class ErrorMessage:
    errors = {
        1000: "داده های ارسالی نامعتبر می باشد",
        1001: "نام کاربری یافت نشد",
        1002: "رمز عبور وارد شده صحیح نمی باشد",
        1003: "کد برای شماره همراه شما ارسال شد",
        1004: "مقادیری وارد نشده است",
        1005: "مقدار عددی باید وارد شود",
        1006: "طول داده ها بیشتر از حد مجاز می باشد",
        1007: "داده وارد شده یکتا نمی باشد",
        1008: "رمز عبور هم خوانی ندارد",
        1009: "مقدار به درستی انتخاب نشد",
        1010: "مقادیر حداقل مجاز می باشد",
        1011: " خطا ناشناخته رخ داده است.به مدیر سایت تماس بگیرید",
        1012 : "این نام کاربری قبلا ثبت نام کرده است",
        1013:"تابحال پستی در این سامانه منتشر نشده است",

    }


class SuccessMessage:
    Success = {
        2000: "عملیات با موفقیت انجام شد",
        2001: "ورود شما با موفقیت اجنام شد",   
        2002: "رای شما به پست مورد نظر ثبت گردید",
    }