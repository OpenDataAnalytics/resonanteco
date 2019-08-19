from girder.api.rest import Resource, setResponseHeader, setContentDisposition, setRawResponse
from girder.api import access, rest
from girder.exceptions import RestException
from girder.api.describe import Description, autoDescribeRoute
from girder.constants import AccessType
from girder.models.collection import Collection
from girder.models.folder import Folder
from girder.models.item import Item


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
        return Item().find({'meta.meta':{'$exists':1}})
