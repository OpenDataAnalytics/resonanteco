import datetime

# from bson.objectid import ObjectId
from girder.api.rest import Resource, setResponseHeader, setContentDisposition, setRawResponse
from girder.api import access, rest
from girder.exceptions import RestException
from girder.api.describe import Description, autoDescribeRoute
from girder.constants import AccessType
from girder.models.collection import Collection
from girder.models.folder import Folder
from girder.models.item import Item
from girder.models.user import User


class Workspace(Resource):
    def __init__(self):
        super(Workspace, self).__init__()
        self.resourceName = 'workspace'

        self.route('GET', (), self.getWorkspace)
        self.route('POST', (), self.createWorkspace)
        self.route('DELETE', (':id',), self.deleteWorkspace)

    @access.user
    @autoDescribeRoute(
        Description('')
        .errorResponse())
    def getWorkspace(self, params):
        user = self.getCurrentUser()
        workspaces = list(Item().findWithPermissions({
            'meta.resonanteco_workspace': True,
        }, user=user, level=AccessType.READ))
        workspaces.sort(key=lambda item: item['updated'], reverse=True)
        return workspaces

    @access.user
    @autoDescribeRoute(
        Description('')
        .jsonParam('workspace', '', requireObject=True, required=True, paramType='body')
        .errorResponse())
    def createWorkspace(self, workspace, params):
        user = self.getCurrentUser()
        private = Folder().createFolder(
            user, 'Private', parentType='user', public=False, creator=user, reuseExisting=True)
        resonantEcoFolder = Folder().createFolder(private, 'ResonantEco', creator=user, reuseExisting=True)
        workspacesFolder = Folder().createFolder(
            resonantEcoFolder, 'Workspaces', creator=user, reuseExisting=True)
        # id = ObjectId.from_datetime(datetime.datetime.now())
        workspaceItem = Item().createItem(workspace['name'], user, workspacesFolder)
        return Item().setMetadata(workspaceItem, {
            'resonanteco_workspace': True, 'datasets': workspace['datasets'], 'filter': workspace['filter']})

    @access.user
    @autoDescribeRoute(
        Description('')
        .modelParam('id', model=Item, destName='workspace', level=AccessType.WRITE)
        .errorResponse())
    def deleteWorkspace(self, workspace, params):
        Item().remove(workspace)
