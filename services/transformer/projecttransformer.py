"""
Data transformer - Project

Source: Project
Target: Frontend
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Table:Project')
class ProjectTransformer(TransformerService):
    """
    Transformer for project data

    Used by: Front - Project data
    """

    def transform(self, data):
        client_transformer = TransformerService.get_transformer('Table:Client')
        region_transformer = TransformerService.get_transformer('Table:Region')
        project_data = []
        for project in data:
            project_data.append({
                'id': project.id,
                'key': project.key,
                'slug': project.slug,
                'label': project.label,
                'description': project.description,
                'location': project.location,
                'region': region_transformer.transform([project.region]),
                'client': client_transformer.transform([project.client]),
                'start_date': project.start_date,
                'end_date': project.end_date,
                'featured': project.featured,
                'service': project.service
            })
