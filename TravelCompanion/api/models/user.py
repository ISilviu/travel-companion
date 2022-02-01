from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Even though django provides a default user model, it was overridden to allow further customizations.
    """
    pass