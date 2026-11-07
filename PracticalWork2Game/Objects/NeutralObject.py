from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Objects.Unit import Unit
from GameObject import GameObject
class NeutralObject(GameObject):
    @abstractmethod
    def interact(self, unit: Unit) -> Unit:
        pass