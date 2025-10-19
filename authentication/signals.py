from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from authentication.models import CustomUserModel

@receiver(post_save,sender=CustomUserModel)
def send_welcome_mail(sender,instance,created,**kwargs):
    if created:
        subject=''
        message=''

        if instance.role=='recruiter':
            subject = 'Welcome to TalentHive - Recruiter'
            message = f'Hi {instance.first_name},\n\nThank you for signing up as a Recruiter on TalentHive. We are excited to have you!Best of luck of finding talents.'

        elif instance.role=='applicant':
            subject = 'Welcome to TalentHive - Applicant'
            message = f'Hi {instance.first_name},\n\nThank you for signing up as an Applicant on TalentHive. We are excited to help you find your dream job!'
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )