from Objects.Unit import Unit
from Objects.Landscape import Landscape
from typing import Optional


class Archer(Unit):
    def __init__(self, name, percent_limit, icon, health, armor, attack, attack_range=3):
        super().__init__(name, percent_limit, icon, health, armor, attack, move_range=1)
        self._attack_range = attack_range

    def move(self, dx: int, dy: int, landscape: Optional[Landscape] = None) -> None:
        if abs(dx) + abs(dy) > self.move_range:
            raise ValueError("Лучник ходит на 1 клетку")

        x, y = self._position
        self._position = (x + dx, y + dy)


    def get_attack_range(self) -> int:
        return self._attack_range