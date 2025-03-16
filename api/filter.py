from django_filters import FilterSet

from api.models import Product


class ProductFilterSet(FilterSet):
    class Meta:
        model = Product
        fields = {
            "name": ["exact", "icontains", "istartswith"],
            "price": ["exact", "range", "lt", "gt"],
            "stock": ["exact", "range", "lt", "gt"],
        }
