from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_resume_created_email(user_email, resume_name):
    send_mail(
        subject='Successfully created your resume',
        message=f'Your resume "{resume_name}" has been created successfully.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )