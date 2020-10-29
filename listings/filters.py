import django_filters
from django import forms
from .models import Listing, Category, CategoryGroup
from .forms import ListingFilterForm


class ListingsFilter(django_filters.FilterSet):
    city = django_filters.MultipleChoiceFilter(
        # choices=CITY_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
    
    categories = django_filters.ModelMultipleChoiceFilter(
        field_name='categories__title',
        to_field_name='title',
        queryset=Category.objects.all().order_by('title'), 
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Listing
        form = ListingFilterForm
        fields = ["city", "categories"]
