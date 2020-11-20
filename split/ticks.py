from django.db.models.signals import post_save
from django.dispatch import receiver

from .consumers import CostConsumer


@receiver(post_save)
def post_save_ws_send(sender, **kwargs):
    instance = kwargs['instance']
    CostConsumer.send([instance])
