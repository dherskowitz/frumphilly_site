import django_filters
from django import forms
from .models import Event, EventCategory
from .forms import EventFilterForm


# cities = Event.objects.values_list('city', flat=True).distinct()
# CITY_CHOICES = [(city, city) for city in cities]


class EventFilter(django_filters.FilterSet):
    city = django_filters.MultipleChoiceFilter(
        # choices=CITY_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )

    categories = django_filters.ModelMultipleChoiceFilter(
        field_name='categories__title',
        to_field_name='title',
        queryset=EventCategory.objects.all().order_by('title'), 
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Event
        form = EventFilterForm
        fields = ["city", "categories"]
