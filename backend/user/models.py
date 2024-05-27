from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUser(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if email is None:
            raise ValueError("The Email field must be set")

        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", True)

        email = self.normalize_email(email)  # Normalize the email address
        user = self.model(email=email, password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db) # Save the user to the database
        return user


    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)


    def create_staff(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUser()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    def __str__(self):
        return self.email.split("@")[0] # Return the username


