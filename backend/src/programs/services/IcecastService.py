import requests
import xml.etree.ElementTree as ET

from django.conf import settings
from datetime import datetime, date, timedelta

from ..models import Program
from ..models import Slot
from ..models import Stats

class IcecastService:

    def __init__(self):
        pass

    @staticmethod
    def get_current_listeners():
        resp = requests.get(settings.ICECAST_AUTODJ_ENDPOINT, auth=('admin', settings.ICECAST_ADMIN_PASSWORD))
        root = ET.fromstring(resp.content)[0]
        count_listeners = 0;
        for child in root.iter('listener'):
            seconds_connected = int(child.find('Connected').text) # Simple bot filter (users that aren't connected all day)
            if seconds_connected < 9000 and seconds_connected > 30:
                count_listeners = count_listeners + 1
        return count_listeners

    @staticmethod
    def get_create_current_stats():
        current_day = date.today()
        current_time = datetime.now().time()
        #Check if there is an active slot
        slot = IcecastService.get_current_active_slot()
        #If there are no active slots, report hourly stats
        if slot == None:
            #Get current hourly report
            query =  Stats.objects.filter(date=current_day, slot=None).order_by('time')
            current_stats_list = [obj for obj in query\
                                 if obj.hour == current_time.hour]
            #print(current_stats_list)
            if len(current_stats_list) > 0:
                #If there is an hourly report, use the latest one available
                current_stats = current_stats_list[-1]
            else:
                #If it does not exist, create the stats for this hourly report
                current_stats = current_stats = Stats.objects.create(slot=None)   
        #If there is an active slot, report stats to that slot
        else:
            try:
                #Get today's stats for this slot
                current_stats = Stats.objects.get(date=current_day, slot=slot) 
            except:
                #If it does not exist, create the stats for this slot
                current_stats = Stats.objects.create(slot=slot)    
        return current_stats

    @staticmethod
    def report_listener_count():
        listener_count = IcecastService.get_current_listeners()
        current_stats = IcecastService.get_create_current_stats()
        current_stats.append(listener_count)
        current_stats.save()
        return True

    @staticmethod
    def get_current_active_slot():
        current_weekday = date.today().isoweekday()
        current_time = datetime.now().time()
        for slot in Slot.objects.filter(time__lte=current_time):
            if slot.program.state == 'A' \
            and slot.iso_weekday == current_weekday \
            and slot.time <= current_time \
            and slot.end_time_obj() >= current_time:
                return slot
        return None
    
