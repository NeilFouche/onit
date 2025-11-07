
from abc import ABC, abstractmethod

from components.graphs import Node

class Segment(ABC):
    def __init__(self, nodes: list[Node | None]) -> None:
        self.path = []

    @abstractmethod
    def execute(self, queryset, request_key):
        """Reduces a segment to a queryset"""