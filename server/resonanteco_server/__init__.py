from girder import plugin

from .rest.record import Record
from .rest.meta import Meta

from .client_webroot import ClientWebroot


class GirderPlugin(plugin.GirderPlugin):
    DISPLAY_NAME = 'ResonantEco server'

    def load(self, info):
        info['serverRoot'], info['serverRoot'].girder = (ClientWebroot(),
                                                         info['serverRoot'])
        info['serverRoot'].api = info['serverRoot'].girder.api
        info['apiRoot'].record = Record()
        info['apiRoot'].meta = Meta()
