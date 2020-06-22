from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from ..managers import CustomUserManager

document_choices = (
    ('CC', _('Citizen Card')),
    ('PP', _('Passport')),
    ('CCo', _('Driving License')),
    ('TR', _('Residence Title')))

student_type_choices = (
    ('Y', _('Yes')),
    ('N', _('Ex-Student')),
    ('E', _('External')))

# The following are not translated, because they are titles particular to the radio
state_choices = (
    ('MM', 'Membro'),
    ('CO', 'Colaborador'),
    ('CH', 'Colaborador Honorário'),
    ('EM', 'Ex-membro'))

department_choices = (
    ('AD', 'Administração'),
    ('CM', 'Comunicação e Marketing'),
    ('PR', 'Programação'),
    ('TL', 'Técnico e Logístico'),
    ('NA', 'Não Atribuído'))

role_choices = (
    ('PR', 'Presidente'),
    ('SE', 'Secretário'),
    ('TE', 'Tesoureiro'),
    ('DI', 'Director'),
    ('EL', 'Elemento'),
    ('NA', 'Não Atribuído'))


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email address'), unique=True)
    is_staff = models.BooleanField(default=False)

    # Profile fields
    author_name = models.CharField(verbose_name=_("Author name"), max_length=75, unique=True)
    full_name = models.CharField(verbose_name=_("Full name"), max_length=100, unique=True)
    id_type = models.CharField(verbose_name=_("ID Type"), max_length=3, choices=document_choices)
    id_number = models.CharField(verbose_name=_("ID Number"), max_length=30, unique=True)
    ist_student_options = models.CharField(verbose_name=_("IST Student"), max_length=1, choices=student_type_choices)
    ist_student_number = models.CharField(verbose_name=_("IST Student Number"), max_length=15, unique=True, null=True,
                                          blank=True)
    phone = models.CharField(verbose_name=_("Phone"), max_length=15, unique=True)
    state = models.CharField(verbose_name=_("State"), max_length=2, choices=state_choices, default="MM")
    entrance_date = models.DateField(verbose_name=_("Entrance Date"), default=timezone.now)
    department = models.CharField(verbose_name=_("Department"), max_length=2, choices=department_choices, default="NA")
    role = models.CharField(verbose_name=_("Role"), max_length=2, choices=role_choices, default="NA")
    notes = models.TextField(verbose_name=_("Notes"), default=None, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    exit_date = models.DateField(verbose_name=_("Exit Date"), default=None, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_registered = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["author_name", "full_name", "id_type", "id_number", "ist_student_options", "phone", "state",
                       "entrance_date"]

    objects = CustomUserManager()


    def __str__(self):
        return self.author_name
