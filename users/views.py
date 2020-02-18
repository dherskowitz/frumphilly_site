from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from events.models import Event


# Create your views here.
@login_required
def user_account(request):
    return render(request, "pages/user/user_account.html")


@login_required
def user_events(request):
    events = Event.objects.filter(created_by=request.user)
    context = {
        "events": events,
    }
    return render(request, "pages/user/user_events.html", context)
