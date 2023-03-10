from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid
from django.db.models import signals
from django.core.mail import send_mail
from django.urls import reverse
from main.tasks import send_verification_email


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email address must be provided')
        if not password:
            raise ValueError('Password must be provided')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    objects = UserAccountManager()
    email = models.EmailField(verbose_name='email', unique=True, blank=False, null=False)
    full_name = models.CharField(verbose_name='full name', blank=True, null=True, max_length=400)
    is_staff = models.BooleanField(verbose_name='staff status', default=False)
    is_active = models.BooleanField(verbose_name='active', default=True)
    is_verified = models.BooleanField(verbose_name='verified', default=False) # Add the `is_verified` flag
    verification_uuid = models.UUIDField(verbose_name='Unique Verification UUID', default=uuid.uuid4().hex)

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email

    def __unicode__(self):
        return self.email


def user_post_save_old(sender, instance, signal, *args, **kwargs):  # Instance ?????? ???????????? user
    if not instance.is_verified:
        # Send verification email
        print('user_post_save', instance.verification_uuid)
        send_mail(
            'Verify your QuickPublisher account',
            'Follow this link to verify your account: '
                'http://localhost:8000%s' % reverse('verify', kwargs={'uuid': str(instance.verification_uuid)}),
            'from@quickpublisher.dev',
            [instance.email],
            fail_silently=False,
        )


def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_verified:
        print('user', instance.pk)
        # Send verification email
        send_verification_email.delay(instance.pk)


signals.post_save.connect(user_post_save, sender=User)
