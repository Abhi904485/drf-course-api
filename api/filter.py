from django_filters import FilterSet

from api.models import Product


class ProductFilterSet(FilterSet):
    class Meta:
        model = Product
        fields = ('name', 'price', 'stock')
