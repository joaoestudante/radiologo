from datetime import datetime, date

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_comma_separated_integer_list

from .slot import Slot

class Stats(models.Model):
    date = models.DateField(verbose_name="Data", auto_now_add=True)
    slot = models.ForeignKey(verbose_name="Slot correspondente às estatísticas", to=Slot, on_delete=models.CASCADE)
    listener_stats_str = models.CharField(verbose_name="Contagens de ouvintes durante a slot", 
    										max_length=360, 
    										default='',
    										validators=[validate_comma_separated_integer_list])

    @property
    def start_time(self):
    	return self.slot.time
    
    @property
    def end_time(self):
    	return self.slot.end_time_obj

    @property 
    def listener_stats_list(self) -> list:
    	string_list = self.listener_stats_str.strip().split(',')
    	if string_list != ['']:
    		return [int(i) for i in string_list]
    	else
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
    	stats_string = ",".join(stats_list)
    	self.listener_stats_str = stats_string

    @staticmethod
    def current_active_slot():
        current_weekday = date.today().isoweekday()
        current_time = datetime.now().time()
        for slot in Slot.objects.all():
            if slot.program.state == 'A' \
            and slot.iso_weekday == current_weekday \
            and slot.time <= current_time \
            and slot.end_time_obj() >= current_time:
            	return slot
        return None

