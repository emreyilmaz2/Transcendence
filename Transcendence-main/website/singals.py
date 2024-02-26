from django.db.models.signals import post_save
from .models import User, Relationship
from django.dispatch import receiver

@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, created, instance, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status =='accepted':
        sender_.friends.add(receiver_)
        receiver_.friends.add(sender_)
        sender_.save()
        receiver_.save()
    