from django.db import models



class OrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('items__product','user')
