from annoying.decorators import render_to
import facebook.djangofb as facebook

from django.db.models import Sum

from profile.models import Profile
from django.contrib.auth.models import User
from logbook.models import Flight

@render_to('facebook_app/canvas.fbml')
@facebook.require_login()
def canvas(request):
    uid = request.facebook.uid

    username = request.POST.get('username', None)
    secret_key = request.POST.get('secret_key', None)


    if username and secret_key:

	p = Profile.goon(user__username=username, secret_key=secret_key)

        if p:
            p.facebook_uid = uid
            p.save()
            message = "You are authenticated!"
        else:
            message = "There was an error :("

    return locals()

@render_to('facebook_app/profile_tab.fbml')
@facebook.require_login()
def profile_tab(request):
    uid = request.facebook.uid
    
    try:
        user = User.objects.get(profile__facebook_uid=uid)
    except User.DoesNotExist:
        user = None

    if user:
        tt = Flight.objects.user(user).sim(False).aggregate(s=Sum('total'))['s']
    else:
        return canvas(request)
    
    return locals()

