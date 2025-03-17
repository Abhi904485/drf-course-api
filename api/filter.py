from django_filters import FilterSet, DateFilter
from rest_framework.filters import BaseFilterBackend

from api.models import Product, Order


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


class OrderFilterSet(FilterSet):
    created_at= DateFilter(field_name="created_at__date")
    class Meta:
        model = Order
        fields = {
            "status": ["exact"],
            "created_at": ["gt", "lt", "exact"],
        }
