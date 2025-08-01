from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Profile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_profile(sender: UserModel, instance: UserModel, created: bool, **kwargs: dict) -> None:
    if created:
        Profile.objects.create(
            pk=instance.pk,
        )
        send_mail(
            subject='Hello and Welcome to Petstagram',
            message='Thank you for registering with Petstagram. We are excited to be part of your journey',
            from_email='settings.COMPANY_EMAIL',
            recipient_list=[instance.email],
        )


