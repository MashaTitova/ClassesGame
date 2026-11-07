from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Tuple
from GameObject import GameObject

from Objects.NeutralObject import NeutralObject
class Unit(GameObject):
    def __init__(self, name: str, percent_limit: int, icon: str,
                 health: int, armor: int, attack: int, move_range: int):
        if not name:
            raise ValueError("Имя не может быть пустым")
        if not (0 < percent_limit < 100):
            raise ValueError(f"Процент юнита на поле вне диапазона [1, 99]")
        if health <= 0:
            raise ValueError("Здоровье должно быть больше 0")
        if armor <= 0 or attack <= 0:
            raise ValueError("Броня и атака должны быть больше 0")

        self.name = name
        self._icon = icon
        self._percent_limit = percent_limit
        self._health = health
        self._max_health = health
        self.armor = armor
        self.attack = attack
        self.move_range = move_range
        self._position: Tuple[int, int] = (0, 0)
        self._gold = 0

    @property
    def icon(self) -> str:
        return self._icon

    @property
    def percent_on_field(self) -> int:
        return self._percent_limit

    @property
    def health(self) -> int:
        return self._health

    @property
    def is_alive(self) -> bool:
        return self._health > 0

    @property
    def position(self) -> Tuple[int, int]:
        return self._position

    def set_position(self, x: int, y: int) -> None:
        self._position = (x, y)

    def take_damage(self, damage: int) -> int:
        actual = max(0, damage - self.armor)
        self._health = max(0, self._health - actual)
        return actual

    def heal(self, amount: int) -> None:
        self._health = min(self._max_health, self._health + amount)

    @abstractmethod
    def move(self, dx: int, dy: int, landscape: "Landscape") -> None:
        pass

    @abstractmethod
    def attack_unit(self, target: "Unit") -> None:
        pass

    @abstractmethod
    def get_attack_range(self) -> int:
        pass

    def __add__(self, other):
        """Юнит + нейтральный объект = взаимодействие"""
        if isinstance(other, NeutralObject):
            return other.interact(self)
        raise TypeError(f"Нельзя сложить юнит с {type(other).__name__}")

    def __repr__(self) -> str:
        return f"{self.name} HP:{self._health}/{self._max_health}"

