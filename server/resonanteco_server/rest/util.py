from bson.objectid import ObjectId

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
            if key == '_id':
                conditions['_id'] = {"$in": [ObjectId(id) for id in filter[key]]}
            elif isinstance(filter[key], list):
                conditions['meta.meta.'+key] = {"$in": filter[key]}
            elif key != 'selectedRegion':
                conditions['meta.'+key] = filter[key]
            if 'selectedRegion' in filter:
                coordinates = filter['selectedRegion']['coordinates'][0]
                conditions['meta.meta.longitude'] = {
                    "$gt": coordinates[0][0], "$lt": coordinates[2][0]}
                conditions['meta.meta.latitude'] = {
                    "$gt": coordinates[0][1], "$lt": coordinates[1][1]}
        matches.append({
            "$match": conditions
        })
    return matches
