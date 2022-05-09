import django_filters

from feedbacks.models import Mobile
from django import forms

class MobileFilter(django_filters.FilterSet):
    # circle = django_filters.CharFilter(lookup_expr='iexact')
    circle = django_filters.CharFilter(lookup_expr='icontains')
    ssa = django_filters.CharFilter(lookup_expr='icontains')
    # upc_date = django_filters.NumberFilter(field_name='upc_date', lookup_expr='year__gt')
    upc_date = django_filters.NumberFilter(field_name='upc_date', lookup_expr='year__lt')
    upc_date__gt = django_filters.NumberFilter(field_name='upc_date', lookup_expr='year__gt')
    # reason_for_PO = django_filters.ModelChoiceFilter(field_name='reason_for_PO', queryset=Mobile.objects.all(), widget=forms.CheckboxSelectMultiple)
    

    class Meta:
        model = Mobile
        fields = ['msisdn', 'circle', 'ssa', 'user']
        