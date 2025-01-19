"""
Data Transformer - Person

Source: Person
"""

from services.transformer import TransformerService


@TransformerService.register_implementation('Get:Person')
class PersonTransformer(TransformerService):
    """
    Transformer for person data

    Purpose: Formatting
    Context: Getting data from the database table: Person
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
