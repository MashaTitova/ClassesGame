from __future__ import annotations
from typing import TYPE_CHECKING

from Objects.Units.Infantry import Infantry
if TYPE_CHECKING:
    from Objects.Unit import Unit

class Swordsman(Infantry):
    def __init__(self):
        super().__init__("Мечник", 20, "⚔️", 100, 10, 15)

    def attack_unit(self, target: Unit) -> None:
        target.take_damage(self.attack)
        print(f"{self.name} атакует {target.name}")