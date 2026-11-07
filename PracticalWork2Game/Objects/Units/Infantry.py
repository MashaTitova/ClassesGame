from Objects.Unit import Unit
from Objects.Landscape import Landscape
from typing import Optional


class Infantry(Unit):
    def __init__(self, name, percent_limit, icon, health, armor, attack):
        super().__init__(name, percent_limit, icon, health, armor, attack, move_range=2)

    def move(self, dx: int, dy: int, landscape: Optional[Landscape] = None) -> None:
        if abs(dx) + abs(dy) > self.move_range:
            raise ValueError("Пехота ходит максимум на 2 клетки")

        x, y = self._position
        self._position = (x + dx, y + dy)

    def get_attack_range(self) -> int:
        return 1