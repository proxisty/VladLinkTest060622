from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Categories(MPTTModel):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(max_length=20)
    alias = models.TextField(max_length=20)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']
