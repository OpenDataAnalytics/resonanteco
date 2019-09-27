import datetime
from girder import events, plugin
from girder.models.user import User
from girder.models.item import Item

from .client_webroot import ClientWebroot
from .rest.record import Record
from .rest.meta import Meta

class GirderPlugin(plugin.GirderPlugin):
    DISPLAY_NAME = 'ResonantEco server'

    def load(self, info):
        # Relocate Girder
        info['serverRoot'], info['serverRoot'].girder = (ClientWebroot(),
                                                         info['serverRoot'])
        info['serverRoot'].api = info['serverRoot'].girder.api
        info['apiRoot'].record = Record()
        info['apiRoot'].meta = Meta()
