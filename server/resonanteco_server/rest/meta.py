from girder.api.rest import Resource, setResponseHeader, setContentDisposition, setRawResponse
from girder.api import access, rest
from girder.exceptions import RestException
from girder.api.describe import Description, autoDescribeRoute
from girder.constants import AccessType
from girder.models.collection import Collection
from girder.models.folder import Folder
from girder.models.item import Item


class Meta(Resource):
    def __init__(self):
        super(Meta, self).__init__()
        self.resourceName = 'meta'

        self.route('GET', (), self.getMeta)
        self.route('GET', ('feature_vs_material',), self.feature_vs_material)

    @access.user
    @autoDescribeRoute(
        Description('')
        .jsonParam('filter', '', requireObject=True, required=False)
        .errorResponse())
    def getMeta(self, filter, params):
        def getAggregation(property):
            pipeline = [
                *getMatchConditions(filter),
                {
                    "$group": {
                        "_id": "$meta.meta.{}".format(property),
                        "count": {
                            "$sum": 1
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "key": {"$ifNull": ["$_id", "other"]},
                        "count": 1
                    }
                }
            ]
            return list(Item().collection.aggregate(pipeline))

        return {
            # 'feature': getAggregation('feature'),
            # 'material': getAggregation('material'),
            'biome': getAggregation('biome'),
            'location': list(Item().collection.aggregate([
                *getMatchConditions(filter),
                {
                    "$match": {
                        "meta.meta.latitude": {
                            "$exists": 1,
                            "$ne": ""
                        },
                        "meta.meta.longitude": {
                            "$exists": 1,
                            "$ne": ""
                        }
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "latitude": "$meta.meta.latitude",
                            "longitude": "$meta.meta.longitude"
                        },
                        "count": {
                            "$sum": 1
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "latitude": "$_id.latitude",
                        "longitude": "$_id.longitude",
                        "count": 1
                    }
                }
            ]))
        }

    @access.user
    @autoDescribeRoute(
        Description('')
        .jsonParam('filter', '', requireObject=True, required=False)
        .errorResponse())
    def feature_vs_material(self, filter, params):
        return list(Item().collection.aggregate([
            *getMatchConditions(filter),
            {
                    "$group": {
                        "_id": {
                            "feature": "$meta.meta.feature",
                            "material": "$meta.meta.material"
                        },
                        "count": {
                            "$sum": 1
                        }
                    }
                    },
            {
                "$project": {
                    "_id": 0,
                    "feature": "$_id.feature",
                    "material": "$_id.material",
                    "count": 1
                }
            }
        ]))


def getMatchConditions(filter):

    matches = [{
        "$match": {
            "meta.meta": {
                "$exists": 1
            }
        }
    }]
    if filter:
        conditions = {}
        for key in filter:
            conditions['meta.meta.'+key] = {"$in": filter[key]}
        matches.append({
            "$match": conditions
        })
    return matches
