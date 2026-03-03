from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=Account)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Our E-commerce Store'
        message = f'Hi {instance.username},\n\nThank you for registering at our store! We are excited to have you on board.\n\nBest regards,\nE-commerce Team'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        
        send_mail(subject, message, from_email, recipient_list)