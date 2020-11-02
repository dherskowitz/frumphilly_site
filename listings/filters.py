import django_filters
from django import forms
from .models import Listing, Category, CategoryGroup
from .forms import ListingFilterForm


class ListingsFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        super(ListingsFilter, self).__init__(*args, **kwargs)

    def get_categories(request):
        return Category.objects.filter(category_group__slug=request.GET['cat_group']).order_by("title")

    city = django_filters.MultipleChoiceFilter(
        widget=forms.CheckboxSelectMultiple
    )

    categories = django_filters.ModelMultipleChoiceFilter(
        field_name='categories__title',
        to_field_name='title',
        queryset=get_categories,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Listing
        form = ListingFilterForm
        fields = ["city", "categories"]
