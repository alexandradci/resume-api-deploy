import os
from celery import shared_task
from django.core.mail import send_mail

print("📧 DEBUG EMAIL_HOST:", os.environ.get("EMAIL_HOST"))
print("📧 DEBUG EMAIL_USER:", os.environ.get("EMAIL_HOST_USER"))


@shared_task
def send_resume_created_email(user_email, resume_name):
    send_mail(
        subject='Successfully created your resume',
        message=f'Your resume "{resume_name}" has been created successfully.',
        from_email='noreply@myresumeapp.com',
        recipient_list=[user_email],
        fail_silently=False,
    )