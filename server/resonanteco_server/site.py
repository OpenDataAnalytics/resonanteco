from itertools import groupby
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


class Site(Resource):
    def __init__(self):
        super(Site, self).__init__()
        self.resourceName = 'site'

        self.route('GET', (), self.getSites)
        self.route('GET', (':name', 'records',), self.getSiteItems)

    @access.user
    @autoDescribeRoute(
        Description('')
        .errorResponse())
    def getSites(self, params):
        datasets = Item().findWithPermissions(
            {'geometa': {'$exists': True}}, user=self.getCurrentUser())
        groups = {}
        for dataset in datasets:
            key = dataset['meta']['metadata']['gold_data']['latitude'] + \
                dataset['meta']['metadata']['gold_data']['longitude']
            if key not in groups:
                groups[key] = []
            groups[key].append(dataset)
        output = []
        for group in groups.values():
            name = group[0]['meta']['metadata']['gold_data']['longitude'] + \
                ','+group[0]['meta']['metadata']['gold_data']['latitude']
            location = {
                'type': 'Point',
                'coordinates': [float(group[0]['meta']['metadata']['gold_data']['longitude']), float(group[0]['meta']['metadata']['gold_data']['latitude'])],
            }
            output.append({'location': location, 'count': len(group), 'name': name})
        return output

    @access.user
    @autoDescribeRoute(
        Description('')
        .errorResponse())
    def getSiteItems(self, name, params):
        [longitude, latitude] = name.split(',')
        return Item().findWithPermissions(
            {'meta.metadata.gold_data.longitude': longitude, 'meta.metadata.gold_data.latitude': latitude}, user=self.getCurrentUser())
