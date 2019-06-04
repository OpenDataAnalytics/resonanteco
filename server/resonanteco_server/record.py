import json

import cherrypy
from geometa.rest import create_geometa
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

        self.route('GET', (':id', 'children',), self.getChildrenRecord)

    @access.user
    @autoDescribeRoute(
        Description('')
        .errorResponse())
    def getChildrenRecord(self, id, params):
        return Item().findWithPermissions(
            {'meta.inputs': id}, user=self.getCurrentUser())
