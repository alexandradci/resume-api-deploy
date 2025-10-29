from django.core.mail.backends.smtp import EmailBackend

class CustomEmailBackend(EmailBackend):
    """Simplified custom backend using Django's secure defaults."""
    pass

