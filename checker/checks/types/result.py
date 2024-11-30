from typing import Any
from dataclasses import dataclass

from .test import Test


@dataclass
class Result:
    test: Test
    percentage: float
