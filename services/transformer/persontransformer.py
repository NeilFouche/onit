"""
Data Transformer - Person

Source: Person
Target: Frontend
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Table:Person')
class PersonTransformer(TransformerService):
    """
    Transformer for person data

    Used by: Front - Person data
    """

    def transform(self, data, *args, **kwargs):
        person_data = []
        for person in data:
            person_data.append({
                "id": person.id,
                "first_name": person.first_name,
                "last_name": person.last_name,
                "initials": person.initials,
                "title": person.title,
                "date_of_birth": person.date_of_birth,
                "phone": person.phone,
                "email": person.email
            })

        return person_data
