from girder.models.model_base import Model


class Table9(Model):
    def initialize(self):
        self.name = 'table9'
        self.ensureIndices(['taxon_oid'])

    def validate(self, doc):
        return doc

    