from datetime import datetime, date, timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_comma_separated_integer_list

from .slot import Slot

class Stats(models.Model):
    date = models.DateField(verbose_name="Data da coleção de contagens", auto_now_add=True)
    time = models.TimeField(verbose_name="Hora de início da coleção de contagens", auto_now_add=True)
    slot = models.ForeignKey(verbose_name="Slot correspondente às contagens, se existir", 
                                null=True,
                                blank=True,
                                to=Slot, 
                                on_delete=models.CASCADE)
    listener_stats_str = models.CharField(verbose_name="Contagens de ouvintes (período 2 min)", 
                                            max_length=360, 
                                            default='',
                                            validators=[validate_comma_separated_integer_list])

    @property
    def hour(self):
        return self.time.hour
    
    @property
    def end_time(self):
        return self.time + timedelta(minutes = 2*len(self.listener_stats_list)-2)

    @property 
    def listener_stats_list(self) -> list:
        string_list = self.listener_stats_str.strip().split(',')
        if string_list != ['']:
            return [int(i) for i in string_list]
        else:
            return []

    @property
    def peak_listeners(self) -> int:
        return max(self.listener_stats_list)

    @property
    def min_listeners(self) -> int:
        return min(self.listener_stats_list)

    @property
    def average_listeners(self) -> float:
        int_list = self.listener_stats_list
        return float(sum(int_list)/len(int_list))

    def append(self, listener_count):
        stats_list = self.listener_stats_list
        stats_list.append(int(listener_count))
        stats_string = ",".join(map(str, stats_list))
        self.listener_stats_str = stats_string



