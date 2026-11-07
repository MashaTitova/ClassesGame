from __future__ import annotations
from typing import List, Type, TYPE_CHECKING

from GameObject import GameObject

if TYPE_CHECKING:
    from Objects.Unit import Unit
class Base(GameObject):
    """База - создаёт юнитов и учитывает их"""

    def __init__(self, name: str, max_health: int, max_units: int, icon: str = "🏰"):
        if not name:
            raise ValueError("Имя базы не может быть пустым")
        if max_health <= 0 or max_units <= 0:
            raise ValueError("Значения должны быть > 0")

        self.name = name
        self._icon = icon
        self._health = max_health
        self._max_health = max_health
        self.max_units = max_units
        self._units: List[Unit] = []

    @property
    def icon(self) -> str:
        return self._icon

    @property
    def percent_on_field(self) -> int:
        return 5

    @property
    def health(self) -> int:
        return self._health

    @property
    def units(self) -> List[Unit]:
        return self._units.copy()

    @property
    def alive_units_count(self) -> int:
        return sum(1 for u in self._units if u.is_alive)

    def create_unit(self, unit_class: Type[Unit]) -> Unit:
        """Создать юнита указанного класса"""
        if self.alive_units_count >= self.max_units:
            raise ValueError(f"Достигнут лимит юнитов ({self.max_units})")

        unit = unit_class()
        self._units.append(unit)
        print(f"{self.name} создала {unit.name}")
        return unit

    def on_unit_destroyed(self, unit: Unit) -> None:
        """Реакция на уничтожение юнита"""
        if unit in self._units:
            self._units.remove(unit)
            print(f"💀 {self.name}: юнит {unit.name} уничтожен")

    def take_damage(self, damage: int) -> None:
        actual = max(0, damage - 10)
        self._health = max(0, self._health - actual)

    def __str__(self) -> str:
        return (
            f"{self.name} [{self._icon}] "
            f"HP:{self._health}/{self._max_health} "
            f"Юнитов:{self.alive_units_count}/{self.max_units}"
        )