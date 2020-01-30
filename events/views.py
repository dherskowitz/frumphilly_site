from django.shortcuts import render
from .models import Event


# Create your views here.
def events(request):
    events = Event.objects.all()
    context = {"events": events}
    return render(request, "pages/events.html", context)
