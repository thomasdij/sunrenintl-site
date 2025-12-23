from django.conf import settings
from .models import Chemical, ChemicalGroup

# Only register the document if OpenSearch is configured
if getattr(settings, 'OPENSEARCH_DSL', {}):
    from django_opensearch_dsl import Document, fields
    from django_opensearch_dsl.registries import registry

    @registry.register_document
    class ChemicalDocument(Document):
        """OpenSearch document for Chemical model."""

        # Index the related ChemicalGroup as a nested object
        group = fields.ObjectField(properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(),
            'slug': fields.KeywordField(),
        })

        # Define custom field configuration for better chemical name matching
        name = fields.TextField(
            attr='name',
            fields={
                'raw': fields.KeywordField(),  # For exact matching
            }
        )

        cas_number = fields.TextField(
            fields={
                'raw': fields.KeywordField(),  # For exact CAS matching
            }
        )

        class Index:
            name = 'chemicals'
            settings = {
                'number_of_shards': 1,
                'number_of_replicas': 0,
            }

        class Django:
            model = Chemical
            fields = [
                'id',
                'slug',
                'hs_code',
                'uses',
            ]
            # Auto-update index when Chemical is saved/deleted
            related_models = [ChemicalGroup]
            # Optimize query with select_related
            queryset_pagination = 100

        def get_instances_from_related(self, related_instance):
            """Update chemicals when their group changes."""
            if isinstance(related_instance, ChemicalGroup):
                return related_instance.chemicals.all()
