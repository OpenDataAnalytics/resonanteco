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


class Soil(Resource):
    def __init__(self):
        super(Soil, self).__init__()
        self.resourceName = 'soil'

        self.route('POST', (':folderId',), self.addMeta)

    @access.user
    @autoDescribeRoute(
        Description('')
        .modelParam(name='folderId', model=Folder, level=AccessType.WRITE)
        .jsonParam('data', '', required=True, paramType='body')
        .errorResponse())
    def addMeta(self, folder, data, params):
        metas = json.loads(data['text'])
        for meta in metas:
            try:
                meta['metadata']['gold_data']['latitude']
            except:
                continue
            item = Item().createItem(meta['_id'], self.getCurrentUser(), folder, meta['file_name'])
            Item().setMetadata(item, meta, allowNull=True)
            # Item().save(item)
            latitude = float(meta['metadata']['gold_data']['latitude'])
            longitude = float(meta['metadata']['gold_data']['longitude'])
            geometa = {
                'crs': '+proj=longlat +datum=WGS84 +no_defs',
                'nativeBounds': {
                    'left': longitude,
                    'right': longitude+0.00001,
                    'bottom': latitude,
                    'top': latitude+0.00001
                },
                'bounds': {
                    'type': 'Polygon',
                    'coordinates': [
                        [
                            [
                                longitude,
                                latitude
                            ],
                            [
                                longitude+0.00001,
                                latitude
                            ],
                            [
                                longitude+0.00001,
                                latitude+0.00001
                            ],
                            [
                                longitude,
                                latitude+0.00001
                            ],
                            [
                                longitude,
                                latitude
                            ]
                        ]
                    ]
                },
                'type_': 'vector',
                'driver': 'OBJ'
            }
            create_geometa(item, None, geometa)
