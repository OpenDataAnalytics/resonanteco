from girder.api.rest import Resource, setResponseHeader, setContentDisposition, setRawResponse
from girder.api import access, rest
from girder.exceptions import RestException
from girder.api.describe import Description, autoDescribeRoute
from girder.constants import AccessType
from girder.models.collection import Collection
from girder.models.folder import Folder
from girder.models.item import Item

from .util import getMatchConditions


class Record(Resource):
    def __init__(self):
        super(Record, self).__init__()
        self.resourceName = 'record'

        self.route('GET', (), self.getAll)
        self.route('GET', ('filtered',), self.getFiltered)

    @access.user
    @autoDescribeRoute(
        Description('')
        .errorResponse())
    def getAll(self, params):
        return Item().find({'meta.meta': {'$exists': 1}})

    @access.user
    @autoDescribeRoute(
        Description('')
        .param('skip', '', default=0, required=False, dataType='number')
        .param('limit', '', default=None, required=False)
        .jsonParam('filter', '', requireObject=True, required=False)
        .jsonParam('fields', '', requireArray=True, required=True)
        .errorResponse())
    def getFiltered(self, filter, fields, skip, limit, params):
        projects = {'$project': {field: '$meta.'+field for field in fields}}
        pipeline = [
            *getMatchConditions(filter),
            projects,
            {"$skip": skip}
        ]
        if limit and int(limit) and int(limit) != -1:
            pipeline.append({
                "$limit": int(limit)
            })
        countRecords = list(Item().collection.aggregate(
            [*getMatchConditions(filter), {"$count": "count"}]))
        count = 0
        if len(countRecords) == 1:
            count = countRecords[0]['count']

        return {"data": list(Item().collection.aggregate(pipeline)),
                "count": count}
