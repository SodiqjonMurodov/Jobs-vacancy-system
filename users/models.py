import random
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import IMAGE_FILE_FORMATS, BaseModel

DARK, LIGHT = ('Dark', 'Light')
ENGLISH, RUSSIAN, UZBEK = ('English', 'Russian', 'Uzbek')
NEW, CONFIRMED, DONE = ('New', 'Confirmed', 'Done')
MALE, FEMALE, OTHER = ('Male', 'Female', 'Other')


class User(AbstractUser, BaseModel):
    class Themes(models.TextChoices):
        DARK = DARK, _('Dark')
        LIGHT = LIGHT, _('Light')

    class Languages(models.TextChoices):
        ENGLISH = ENGLISH, _('English')
        RUSSIAN = RUSSIAN, _('Russian')
        UZBEK = UZBEK, _('Uzbek')

    class AuthStatus(models.TextChoices):
        NEW = NEW, _('New')
        CONFIRMED = CONFIRMED, _('Confirmed')
        DONE = DONE, _('Done')

    class Genders(models.TextChoices):
        MALE = MALE, _('Male')
        FEMALE = FEMALE, _('Female')
        OTHER = OTHER, _('Other')

    username = models.CharField(max_length=255, unique=False, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(_("phone number"), max_length=14, blank=True, null=True)
    auth_status = models.CharField(_("auth status"), max_length=10, choices=AuthStatus.choices, default=AuthStatus.NEW)
    date_of_birth = models.DateField(_("date of birth"), blank=True, null=True)
    gender = models.CharField(_("gender"), max_length=6, choices=Genders.choices, default=Genders.OTHER)
    image = models.ImageField(_('profile image'), upload_to='profile', null=True, blank=True,
                              validators=[FileExtensionValidator(IMAGE_FILE_FORMATS)])
    description = models.TextField(_("description"), null=True, blank=True)
    region = models.ForeignKey('common.Region', on_delete=models.CASCADE, null=True, blank=True)
    custom_region = models.ForeignKey('common.CustomRegion', on_delete=models.CASCADE, null=True, blank=True)
    theme = models.CharField(_("theme"), max_length=5, choices=Themes.choices, default=Themes.LIGHT)
    language = models.CharField(_("language"), max_length=12, choices=Languages.choices, default=Languages.RUSSIAN)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return f'{self.email}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name_plural = _('Users')
        verbose_name = _('User')

    def create_verify_code(self):
        code = "".join([str(random.randint(0, 100) % 10) for _ in range(4)])
        while UserConfirmation.objects.filter(code=code).exists():
            code = "".join([str(random.randint(0, 100) % 10) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id=self.pk,
            code=code
        )
        return code


EMAIL_EXPIRE_TIME = 2


class UserConfirmation(BaseModel):
    code = models.CharField(max_length=4)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    expiration_time = models.DateTimeField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = _('User Confirmation')
        verbose_name_plural = _('User Confirmations')

    def save(self, *args, **kwargs):
        if not self.pk or self.is_confirmed == False:
            self.expiration_time = datetime.now() + timedelta(minutes=EMAIL_EXPIRE_TIME)
        super(UserConfirmation, self).save(*args, **kwargs)

