from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, verbose_name=_('user'))
    first_name = models.CharField(max_length=30, null=True, blank=True, verbose_name=_('first name'))
    last_name = models.CharField(max_length=30, null=True, blank=True, verbose_name=_('last name'))
    balance = models.IntegerField(default=0, verbose_name=_('balance'))

    class Meta:
        verbose_name_plural = _('profiles')
        verbose_name = _('profile')


@receiver(post_save, sender=User)
def profile_create(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance, first_name=instance.username)
        profile.save()
