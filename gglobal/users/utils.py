from allauth.account import app_settings, signals
from allauth.account.utils import perform_login

def complete_signup(request, user, email_verification, success_url,
                    signal_kwargs=None):
    if signal_kwargs is None:
        signal_kwargs = {}
    signals.user_signed_up.send(sender=user.__class__,
                                request=request,
                                user=user,
                                **signal_kwargs)
    return perform_login(request, user,
                         email_verification=email_verification,
                         signup=False,
                         redirect_url=success_url,
                         signal_kwargs=signal_kwargs)