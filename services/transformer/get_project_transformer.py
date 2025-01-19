"""
Data transformer - Project

Source: Project
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Get:Project')
class ProjectTransformer(TransformerService):
    """
    Transformer for project data

    Purpose: Formatting
    Context: Getting data from the database table: Project
    """

    def transform(self, data, *args, **kwargs):
        client_transformer = TransformerService.get_transformer("Get:Client")
        region_transformer = TransformerService.get_transformer("Get:Region")
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
