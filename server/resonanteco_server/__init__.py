from girder import plugin

from .rest.record import Record
from .rest.meta import Meta
from .rest.workspace import Workspace


class GirderPlugin(plugin.GirderPlugin):
    DISPLAY_NAME = 'ResonantEco server'

    def load(self, info):
        info['apiRoot'].record = Record()
        info['apiRoot'].meta = Meta()
        info['apiRoot'].workspace = Workspace()
