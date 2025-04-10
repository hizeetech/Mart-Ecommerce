# vendor/decorators.py
from django.http import HttpResponseForbidden

def check_role_vendor(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'vendor'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not allowed to access this page.")
    return wrapper_func
