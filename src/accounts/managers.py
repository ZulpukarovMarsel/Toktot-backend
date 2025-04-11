from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
            self, phone,  password,
            is_staff, is_superuser,
            **extra_fields
    ):
        now = timezone.now()
        user = self.model(
            phone=phone,
            is_staff=is_staff,
            is_superuser=is_superuser,
            date_joined=now,
            **extra_fields
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        return self._create_user(
            phone, password, False, False, **extra_fields
        )

    def create_superuser(self, phone, password=None, **extra_fields):
        user = self._create_user(
            phone, password, True, True, **extra_fields
        )
        user.save(using=self._db)
        return user
