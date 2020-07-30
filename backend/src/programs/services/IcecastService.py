import requests
import xml.etree.ElementTree as ET

from django.conf import settings
from ..models import Program
from ..models import Slot

class IcecastService:

  @staticmethod
  def get_current_listeners():
    resp = requests.get(settings.ICECAST_AUTODJ_ENDPOINT, auth=('admin', settings.ICECAST_ADMIN_ENDPOINT))
    root = ET.fromstring(resp.content)[0]
    count_listeners = 0;
    for child in root.iter('listener'):
        seconds_connected = int(child.find('Connected').text) # Simple bot filter (users that aren't connected all day)
        if seconds_connected < 9000 and seconds_connected > 30:
            count_listeners = count_listeners + 1
    return count_listeners
    
