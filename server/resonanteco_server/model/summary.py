from girder.models.model_base import Model


class Summary(Model):
    def initialize(self):
        self.name = 'summary'
        self.ensureIndices(['taxon_oid'])

    def validate(self, doc):
        return doc

    