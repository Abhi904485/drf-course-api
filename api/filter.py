from django_filters import FilterSet
from rest_framework.filters import BaseFilterBackend

from api.models import Product


class InStockProductFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)

class ProductFilterSet(FilterSet):
    class Meta:
        model = Product
        fields = {
            "name": ["exact", "icontains", "istartswith"],
            "price": ["exact", "range", "lt", "gt"],
            "stock": ["exact", "range", "lt", "gt"],
        }
