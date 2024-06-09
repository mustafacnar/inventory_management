from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from products.models import Product


@receiver(post_save, sender=Product)
def update_bundles_stock(sender, instance, **kwargs):
    for bundle in instance.bundle_set.all():
        bundle.stock = min([product.product_quantity for product in bundle.products.all()])
        bundle.save()


@receiver(pre_delete, sender=Product)
def delete_related_bundles(sender, instance, **kwargs):
    instance.bundle_set.all().delete()
