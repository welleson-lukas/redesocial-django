from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Perfil, Relationship

@receiver(post_save, sender=User)
def post_save_create_perfil(sender, instance, created, **kwargs):
    print('sender', sender)
    print('instance', instance)
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'aceita':
        sender_.amigos.add(receiver_.user)
        receiver_.amigos.add(sender_.user)
        sender_.save()
        receiver_.save()