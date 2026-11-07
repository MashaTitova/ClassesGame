from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Objects.Unit import Unit
class Landscape(ABC):
    @property
    @abstractmethod
    def icon(self) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def can_enter(self, unit: Unit) -> bool:
        pass

    @abstractmethod
    def apply_effect(self, unit: Unit) -> None:
        pass