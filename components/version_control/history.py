"""
On It Version Control - History Manager

Manages the historical state of an entity
"""

from services.database import DatabaseService


class History:
    """Manages the historical state of an entity"""

    def __init__(self, entity, field=None, value=None):
        self.entity = entity
        self._field = field
        self._value = value
        self.history = self._load_states()
        self._database = DatabaseService.get_database()

    def push(self, state):
        """
        Adds a state to the history

        Args:
            state (EntityState): The state to add
        """
        self._database.entity_state.create(state.to_dict())
        self.history.append(state)

    def pop(self):
        """
        Removes the last state from the history.

        Returns:
            EntityState: The last state
        """
        instance = self.history.pop()
        self._database.entity_state.delete(instance.to_dict())

        return instance

    def _load_states(self):
        """
        Loads the states from the database.

        Returns:
            list: The list of states
        """
        field = self._field or "pk"
        value = self._value or self.entity["id"]
        states = self._database.entity_state.filter({field: value})

        return states
