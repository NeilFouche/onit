
from components.graphs import Node
from components.graphs.segments import ChainSegment, IntermediateSegment, Segment
from components.processors import Query
from components.sources import Source
from libs.algorithms import a_star
from services.data import DataService
from services.database import DatabaseService
from services.processing import TransformationService
from services.rest import RestService

@DataService.register_source("Database:Default")
class RelationalDatabaseSource(Source):
    """Data source for data stored in the database"""

    def __init__(self, label="Database") -> None:
        self.label = label
        self.database = DatabaseService.get_database()

    def fetch(self, request_key: str):
        """
        Fetch data from target table by finding and traversing the relationship
        path from source table.

        Target table: Whose records will be returned
        Source table: The table where filters are applied (defaults to target)
        Filter params: Query filters applied to the source table

        Args:
            request_key (str): Key for getting access to the applicable request.

        Returns:
            queryset (QuerySet): A queryset for the target records
        """
        try:
            filter_params = RestService.get_query_parmeters(request_key)

            target = RestService.get_command_target(request_key)
            target_tables = target.split('-')
            target = target_tables[0]
            source = target_tables[1] if len(target_tables) == 2 else target

            graph = self.database.schema_graph
            path = a_star(graph, source, target)
            optimized_path = self.optimize_path(path)
            queryset = self.execute_path(source, optimized_path, filter_params, request_key)

            post_processor = TransformationService.get_processor(f"Get:{target}")
            data = post_processor.transform(queryset, request_key=request_key)

        except ValueError:
            print(f"The target specified is invalid: {target}")
        except Exception as e:
            print(f"Unable to process request: {e}")
            raise e

        return data

    def optimize_path(self, path: list[Node]) -> list[Segment]:
        """
        Converts raw A* path into optimized segments.
        Returns list of PathSegment objects (chain or intermediate)
        """
        segments = []
        current_chain: list[Node] = []

        for i, node in enumerate(path):
            node_table = self.database.get(model_name=node.name)

            if node_table.table_type == 'intermediate':
                if current_chain:
                    segments.append(ChainSegment(current_chain, path))
                    current_chain = []

                segments.append(IntermediateSegment(
                    nodes=[
                        path[i+1] if i > 0 else None,
                        node,
                        path[i-1] if i < len(path)-1 else None
                    ],
                    path=path
                ))
            else:
                current_chain.append(node)

        if current_chain:
            segments.append(ChainSegment(current_chain, path))

        return segments

    def execute_path(self, source_table_name: str, segments: list[Segment], parameters: dict, request_key: str):
        """Execute the optimized path segments"""
        builder = Query.get_builder()
        query = builder.fit(parameters)
        queryset = self.database.get(model_name=source_table_name).filter(query, request_key)

        for segment in reversed(segments):
            queryset = segment.execute(queryset, request_key)

        return queryset