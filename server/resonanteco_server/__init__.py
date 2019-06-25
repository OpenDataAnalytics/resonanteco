import datetime
from girder import events, plugin
from girder.models.user import User
from girder.models.item import Item

from .client_webroot import ClientWebroot
from .soil import Soil

class GirderPlugin(plugin.GirderPlugin):
    DISPLAY_NAME = 'ResonantEco server'

    def load(self, info):
        # Relocate Girder
        info['serverRoot'], info['serverRoot'].girder = (ClientWebroot(),
                                                         info['serverRoot'])
        info['serverRoot'].api = info['serverRoot'].girder.api
        info['apiRoot'].soil = Soil()
