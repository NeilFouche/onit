
from django.db.models import QuerySet
from typing import cast

from onit.constants import EMPTY_QUERYSET
from components.sources.databases import Table
from components.graphs import Node
from components.graphs.segments import Segment
from libs.strings import format_str
from services.database import DatabaseService

class IntermediateSegment(Segment):
    def __init__(self, nodes: list[Node | None], path):
        self.predecessor, self.intermediate, self.successor = nodes
        self.path = path

        self.intermediate_table: Table
        self.predecessor_table: Table
        self.successor_table: Table


    def execute(self, queryset, request_key) -> QuerySet:
        if self.intermediate is None:
            return cast(QuerySet, EMPTY_QUERYSET)

        db = DatabaseService.get_database()
        self.intermediate_table = db.get(model_name=self.intermediate.name)

        if self.predecessor:
           from_left = self.predecessor.name == self.intermediate_table.dependent_table
           self.predecessor_table = db.get(model_name=self.predecessor.name)
           queryset = self.resolve_predecessor_to_intermediate(queryset, request_key, from_left)

        if self.successor:
            from_left = self.successor.name != self.intermediate_table.dependent_table
            self.successor_table = db.get(model_name=self.successor.name)
            queryset = self.resolve_intermediate_to_successor(queryset, request_key, from_left)

        return queryset.distinct()


    def resolve_predecessor_to_intermediate(self, queryset, request_key, from_left = True):
        """
        Two-Way Join: Predecessor -> Intermediate.
        Returns a QuerySet of the Intermediate model.
        """
        predecessor_qs = queryset
        predecessor_ids = predecessor_qs.values_list("id", flat=True)
        self.predecessor_table.set_queryset(request_key, predecessor_qs)

        foreign_key = self.intermediate_table.get_related_name(self.intermediate_table.dependent_table)
        generic_foreign_key = "object_id"

        # Handle left vs right
        related_name = foreign_key if from_left else generic_foreign_key

        if from_left:
            intermediate_filter = {
                f"{related_name}__in": predecessor_ids
            }
        else:
            intermediate_filter = {
                f"{related_name}__in": predecessor_ids,
                "content_type__model": format_str(self.predecessor_table.model_name)
            }

        intermediate_qs = self.intermediate_table.all()
        intermediate_qs = intermediate_qs.filter(**intermediate_filter).distinct()
        self.intermediate_table.set_queryset(request_key, intermediate_qs)

        return intermediate_qs

    def resolve_intermediate_to_successor(self, queryset, request_key, from_left = True):
        """
        Two-Way Join: Intermediate -> Successor
        Returns a QuerySet of the Successor model.
        """
        if from_left:
            queryset = queryset.filter(content_type__model=format_str(self.successor_table.model_name))
            self.intermediate_table.set_queryset(request_key, queryset)

        foreign_key = self.intermediate_table.get_related_name(self.intermediate_table.dependent_table)
        generic_foreign_key = "object_id"
        target_name = generic_foreign_key if from_left else foreign_key

        intermediate_qs = queryset
        successor_ids = intermediate_qs.values_list(target_name, flat=True)
        successor_qs = self.successor_table.all()

        queryset = successor_qs.filter(pk__in=successor_ids).distinct()
        self.successor_table.set_queryset(request_key, queryset)

        return queryset
