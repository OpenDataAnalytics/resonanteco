from girder.models.model_base import Model


class Table8(Model):
    def initialize(self):
        self.name = 'table8'
        self.ensureIndices(['taxon_oid'])

    def validate(self, doc):
        return doc

    