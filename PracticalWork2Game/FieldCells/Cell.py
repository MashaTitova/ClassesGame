from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from Objects.Landscape import Landscape

if TYPE_CHECKING:
    from Objects.Unit import Unit
    from Objects.NeutralObject import NeutralObject
    from Objects.Base import Base


class Cell:
    def __init__(self, landscape: Landscape):
        self.landscape = landscape
        self.unit: Optional[Unit] = None
        self.neutral: Optional[NeutralObject] = None
        self.base: Optional[Base] = None

    def is_passable(self, unit: Unit) -> bool:
        """Может ли юнит войти на клетку."""
        if self.unit is not None or self.base is not None:
            return False
        return self.landscape.can_enter(unit)

    def __str__(self) -> str:
        if self.base:
            return self.base.icon
        if self.unit:
            return self.unit.icon
        if self.neutral:
            return self.neutral.icon
        return self.landscape.icon