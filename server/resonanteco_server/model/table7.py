from girder.models.model_base import Model


class Table7(Model):
    def initialize(self):
        self.name = 'table7'
        self.ensureIndices(['taxon_oid'])

    def validate(self, doc):
        return doc

    