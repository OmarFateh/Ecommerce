from django.shortcuts import redirect, resolve_url
from django.utils.http import is_safe_url
from django.conf import settings


def redirect_after_login(request):
    """
    Redirect user after login to the previous url.
    """
    url_path = request.GET.get("next", None) 
    if url_path is None:
        return redirect(settings.LOGIN_REDIRECT_URL)
    elif not is_safe_url(
            url=resolve_url(url_path),
            allowed_hosts={request.get_host()},
            require_https=request.is_secure()
        ):
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return redirect(resolve_url(url_path))