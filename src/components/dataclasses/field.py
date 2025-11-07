from dataclasses import dataclass
from django.db import models
from typing import Optional

@dataclass
class TableField:
    name: str
    model: models.Field
    is_related: bool = False
    is_many_to_many: bool = False
    related_name: Optional[str] = None