from django.shortcuts import redirect


def unauthenticated_user(view_func):
    """
    Restrict the user from visiting certain pages if already logged in,
    Redirect to another page. 
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:    
            return view_func(request, *args, **kwargs)
    return wrapper_func  