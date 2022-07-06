from dataclasses import dataclass, field
from pathlib import Path

from quantities import Table


@dataclass
class Problem:
    id_: str
    path: Path
    statement: str
    solution: str = None
    answer: list[str] = field(default_factory=list)
    choices: list[str] = field(default_factory=list)
    obj: int = None
    constants: Table = field(default_factory=Table)
    data: Table = field(default_factory=Table)
