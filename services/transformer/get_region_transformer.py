"""
Data Transformer - Region

Source: Region
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Get:Region')
class RegionTransformer(TransformerService):
    """
    Transformer for region data

    Purpose: Formatting
    Context: Getting data from the database table: Region
    """

    def transform(self, data, *args, **kwargs):
        region_data = []
        for region in data:
            region_data.append({
                "id": region.id,
                "key": region.key,
                "slug": region.slug,
                "label": region.label,
                "description": region.description,
                "capital": region.capital,
                "population": region.population,
            })

        return region_data
