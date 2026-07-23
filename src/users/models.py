from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from  enums.enums import Gender, Role, Language
class Player(AbstractUser):
    email = models.EmailField(_('email address'),unique= True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    role = models.CharField(max_length=20, choices=Role.choices(),
                            default=Role.USER.value)
    language = models.CharField(max_length=20, choices=Language.choices(),
                                default=Language.UK.value)
    gender = models.CharField(max_length=20, choices=Gender.choices(),
                              default=Gender.M.value)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username