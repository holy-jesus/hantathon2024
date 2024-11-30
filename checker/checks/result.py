from typing import Any
from enum import Enum
from dataclasses import dataclass

from .test import Test


class Type(Enum):
    pass


@dataclass
class Result:
    test: Test
    value: Any
