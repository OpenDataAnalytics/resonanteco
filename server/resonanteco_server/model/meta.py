from girder.models.model_base import Model


class Meta(Model):
    def initialize(self):
        self.name = 'meta'
        self.ensureIndices(['taxon_oid'])

    def validate(self, doc):
        return doc

    