from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from unidecode import unidecode


DURATIONS = (
    (28, '28'),
    (57, '57'),
    (117, '117'),
)

STATES = (
    ('A', 'Activo'),
    ('H', 'Em hiato'),
    ('T', 'Terminado')
)


class Program(models.Model):
    name = models.CharField(verbose_name="Nome", max_length=200, default="", unique=True)
    description = models.CharField(verbose_name="Descrição", max_length=500, default="")
    authors = models.ManyToManyField(get_user_model(), verbose_name="Autores", blank=True)
    max_duration = models.IntegerField(verbose_name="Duração Máxima", default=28, choices=DURATIONS)
    first_emission_date = models.DateTimeField(verbose_name="Primeira emissão", default=timezone.now)
    comes_normalized = models.BooleanField(verbose_name="Não aplicar alteração dinâmica de volume", default=False,
                                           help_text="Caso o programa tenha certas partes propositadamente baixas, "
                                                     "selecciona esta opção.")
    ignore_duration_adjustment = models.BooleanField(verbose_name="Ignorar ajuste automático de duração", default=False,
                                                     help_text=" "
                                                               "Caso o programa não deva ter a sua duração ajustada "
                                                               "automaticamente, selecciona esta opção.")
    is_external = models.BooleanField(default=False)
    state = models.CharField(verbose_name="Estado", choices=STATES, default="A", max_length=15)

    def __str__(self):
        return self.name

    def normalized_name(self):
        return unidecode(''.join(c for c in self.name if c.isalnum()).lower())
