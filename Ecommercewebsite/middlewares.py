from django.shortcuts import HttpresponseRedirect
from django.urls import resolve
# resolve takes complete path and resolve it with the name of tha path.
def login_register_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        url_name = resolve(request.path_info).url_name
        if (url_name =='login' or url_name =='signup') and request.user.is_authenticated:
            response = HttpresponseRedirect('shop/profile')

        else:
            response = get_response(request)
    
        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware