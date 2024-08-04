from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(
        self, email, first_name, last_name, phone_number, role, password=None
    ):
        if not email:
            raise ValueError(_("The Email field must be set"))
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            role=role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, first_name, last_name, phone_number, role, password=None
    ):
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            role=role,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    id_user = models.AutoField(primary_key=True)
    role = models.CharField(
        max_length=50,
        choices=[
            ("admin", "Admin"),
            ("staff", "Staff"),
            # Add other roles as needed
        ],
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number", "role"]

    def __str__(self):
        return self.email
