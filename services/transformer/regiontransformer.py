"""
Data Transformer - Region

Source: Region
Target: Frontend
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Table:Region')
class RegionTransformer(TransformerService):
    """
    Transformer for region data

    Used by: Front - Region data
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
