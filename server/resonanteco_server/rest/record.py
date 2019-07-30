from girder.api.rest import Resource, setResponseHeader, setContentDisposition, setRawResponse
from girder.api import access, rest
from girder.exceptions import RestException
from girder.api.describe import Description, autoDescribeRoute
from girder.constants import AccessType
from girder.models.collection import Collection
from girder.models.folder import Folder
from girder.models.item import Item

from ..model.meta import Meta
from ..model.summary import Summary
from ..model.table7 import Table7
from ..model.table8 import Table8
from ..model.table9 import Table9


class Record(Resource):
    def __init__(self):
        super(Record, self).__init__()
        self.resourceName = 'record'

        self.route('GET', (), self.getAll)

    @access.user
    @autoDescribeRoute(
        Description('')
        .errorResponse())
    def getAll(self, params):
        return {
            'meta': list(Meta().find()),
            'summary': list(Summary().find()),
            'table7': list(Table7().find()),
            'table8': list(Table8().find()),
            'table9': list(Table9().find())
        }
