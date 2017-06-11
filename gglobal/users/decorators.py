from django.conf import settings
from gglobal.crm.models import ExecutantProfile
from django.core.exceptions import ObjectDoesNotExist

def executants_required(function=None, home_url=None, redirect_field_name=None):
    """Check that the user is NOT logged in.

    This decorator ensures that the view functions it is called on can be 
    accessed only by anonymous users. When an authenticated user accesses
    such a protected view, they are redirected to the address specified in 
    the field named in `next_field` or, lacking such a value, the URL in 
    `home_url`, or the `USER_HOME_URL` setting.
    """
    if home_url is None:
        home_url = settings.EXECUTANT_HOME_URL

    def _dec(view_func):
        def _view(request, *args, **kwargs):
            try:
                executant = ExecutantProfile.objects.get(user = request.user)
            except ObjectDoesNotExist:
                executant == None
            if executant:
                url = None
                if redirect_field_name and redirect_field_name in request.REQUEST:
                    url = request.REQUEST[redirect_field_name]
                if not url:
                    url = home_url
                if not url:
                    url = "/"
                return HttpResponseRedirect(url)
            else:
                return view_func(request, *args, **kwargs)

        _view.__name__ = view_func.__name__
        #_view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)





from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from gglobal.users.models import User


def master_required(function):
    def wrapper(request, *args, **kwargs):
        decorated_view_func = login_required(request)
        if not decorated_view_func.user.is_authenticated():
            return decorated_view_func(request)  # return redirect to signin

        master = User.objects.filter(mastercrmprofile__isnull=False)
        if not master:  # if not coach redirect to home page
            return HttpResponseRedirect(reverse('home', args=(), kwargs={}))
        else:
            return function(request, *args, master=master, **kwargs)

    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper