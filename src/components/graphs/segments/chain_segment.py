

from components.graphs import Node
from components.graphs.segments import Segment
from services.database import DatabaseService

class ChainSegment(Segment):
    def __init__(self, nodes: list[Node], path):
        self.nodes = nodes
        self.path = path

    def execute(self, queryset, request_key):
        ids = queryset.values_list("id", flat=True)

        if not self.path:
            return []

        # Build query_key_string from query_path
        query_keys = []
        for i, node in enumerate(self.nodes):
            # Break on the last node
            if i == len(self.nodes) - 1:
                break

            query_keys.append(node.foreign_key)

        query_keys.append('id__in')
        query_key_string = '__'.join(query_keys)
        filter_params = {f"{query_key_string}": ids}

        # Fetch the data
        target_model_name = self.nodes[0].name
        db = DatabaseService.get_database()

        return db.get(model_name=target_model_name).filter(**filter_params, request_key=request_key).distinct()