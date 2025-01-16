"""
On It Version Control - Entity State

Represents the state of an entity
"""

from datetime import datetime


class EntityState:
    """Represents the state of an entity"""

    def __init__(self, table, entity):
        self.table = table
        self.entity_id = entity["entity_id"]
        self.key = entity["entity_key"]
        self.value = entity["value"]
        self.created_date = datetime.now()

    def to_dict(self):
        """
        Method to convert the state to a dictionary.
        """
        return {
            "table": self.table,
            "entity_id": self.entity_id,
            "entity_key": self.key,
            "value": self.value,
            "created_date": self.created_date
        }
