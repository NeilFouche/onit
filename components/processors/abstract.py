from abc import ABC
from typing import Any, Optional

class Processor(ABC):

    def fit(self, request_key, *args, **kwargs) -> dict[str, Any]:
        """Sets up the processor for transformation."""
        return {}

    def inverse_transform(self, request_key, *args, **kwargs):
        """Reverses or applies the inverse operation of the transformation."""

    def transform(self, data, request_key: Optional[str] = None, *args, **kwargs) -> Any:
        """Performs the transformation on the data."""
