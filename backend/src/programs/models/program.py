from functools import cached_property

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from unidecode import unidecode
from datetime import timedelta, date, datetime

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
    rss_feed_status = models.BooleanField(verbose_name="Status do upload automático com Feed RSS", default=False)
    rss_feed_url = models.CharField(max_length=1024, verbose_name="Endereço do Feed RSS", default="")

    def __str__(self):
        return self.name

    def normalized_name(self):
        return unidecode(''.join(c for c in self.name if c.isalnum()).lower())

    @cached_property
    def disabled_days(self) -> tuple:
        # Return non-intersecting elements
        return tuple(set(self.enabled_days).symmetric_difference({1, 2, 3, 4, 5, 6, 7}))

    @cached_property
    def enabled_days(self) -> tuple:
        return tuple([slot.iso_weekday for slot in self.slot_set.all().order_by('weekday')])

    @cached_property
    def occupied_slots(self) -> dict:
        result = {}
        for slot in self.slot_set.all():
            result[slot.iso_weekday] = slot.internal_slots_occupied()
        return result

    def next_emission_date(self) -> str:  # the actual next date an emission should play
        current_day = date.today()
        current_iso_weekday = current_day.isoweekday()
        if current_iso_weekday in self.enabled_days:
            return current_day.isoformat()
        else:
            for i in range(1, 7):
                if (current_day + timedelta(days=i)).isoweekday() in self.enabled_days:
                    return (current_day + timedelta(days=i)).isoformat()

    def next_upload_date(self) -> str:  # the next date an emission should be uploaded to
        from programs.services.RemoteService import \
            RemoteService  # it's here to avoid circular imports when initializing

        uploaded_dates = RemoteService().get_uploaded_dates(self)
        start = date.today()
        for i in range(52):
            for i in range(7):
                day = start + timedelta(days=i)
                if day.isoweekday() in self.enabled_days and day.strftime("%Y-%m-%d") not in uploaded_dates:
                    return day.isoformat()
            start = start + timedelta(days=7)

    def get_filename_for_date(self, date: str):
        from programs.services.ProgramService import ProgramService
        if len(date) == 9:  # includes weekday
            return self.normalized_name() + date + ".mp3"
        else:
            return self.normalized_name() + date + ProgramService().get_weekday_for_date(self.slot_set,
                                                                                         self.enabled_days,
                                                                                         date) + ".mp3"
