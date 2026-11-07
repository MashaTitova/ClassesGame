from __future__ import annotations
import copy
from typing import List, TYPE_CHECKING, Optional

from FieldCells.Cell import Cell
from Objects.Landscapes.Plain import Plain

if TYPE_CHECKING:
    from Objects.Unit import Unit
    from Objects.NeutralObject import NeutralObject
    from Objects.Landscape import Landscape
    from Objects.Base import Base

class Field:
    def __init__(self, width: int, height: int, max_capacity: int):
        if not (5 <= width <= 30 and 5 <= height <= 30):
            raise ValueError("Размеры поля: от 5 до 30")
        if max_capacity <= 0:
            raise ValueError("Вместимость должен быть > 0")

        self._width = width
        self._height = height
        self._max_capacity = max_capacity
        self._grid: list[list[Cell]] = [
            [Cell(Plain()) for _ in range(width)] for _ in range(height)
        ]
        self._current_count = 0

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def set_landscape(self, x: int, y: int, landscape: Landscape) -> None:
        self._check_position(x, y)
        self._grid[y][x].landscape = landscape

    def place_unit(self, x: int, y: int, unit: Unit) -> None:
        self._check_position(x, y)
        cell = self._grid[y][x]

        if not cell.is_passable(unit):
            raise ValueError(f"Клетка ({x}, {y}) непроходима или занята")

        if self._current_count >= self._max_capacity:
            raise ValueError(f"Превышен лимит объектов ({self._max_capacity})")

        # Проверяем лимит по типу
        type_count = self._count_type(type(unit))
        if type_count >= unit.percent_on_field:
            raise ValueError(f"Превышен лимит типа {type(unit).__name__}")

        cell.unit = unit
        unit.set_position(x, y)
        self._current_count += 1

        # Применяем эффект ландшафта
        cell.landscape.apply_effect(unit)

    def place_base(self, x: int, y: int, base: Base) -> None:
        """Разместить базу на поле."""
        self._check_position(x, y)
        cell = self._grid[y][x]
        if cell.base is not None:
            raise ValueError(f"Клетка ({x}, {y}) уже занята базой")
        cell.base = base
        print(f" База размещена на ({x}, {y})")

    def remove_base(self, x: int, y: int) -> None:
        self._check_position(x, y)
        self._grid[y][x].base = None

    def place_neutral(self, x: int, y: int, obj: NeutralObject) -> None:
        self._check_position(x, y)
        cell = self._grid[y][x]
        if cell.neutral or cell.unit:
            raise ValueError("Клетка занята")
        cell.neutral = obj
        self._current_count += 1

    def remove_unit(self, x: int, y: int) -> Optional[Unit]:
        self._check_position(x, y)
        cell = self._grid[y][x]
        if cell.unit:
            unit = cell.unit
            cell.unit = None
            self._current_count -= 1
            return unit
        return None

    def remove_neutral(self, x: int, y: int) -> Optional[NeutralObject]:
        self._check_position(x, y)
        cell = self._grid[y][x]
        if cell.neutral:
            obj = cell.neutral
            cell.neutral = None
            self._current_count -= 1
            return obj
        return None

    def get_cell(self, x: int, y: int) -> Cell:
        self._check_position(x, y)
        return self._grid[y][x]

    def _check_position(self, x: int, y: int) -> None:
        if not (0 <= x < self._width and 0 <= y < self._height):
            raise IndexError(f"Координаты ({x}, {y}) вне диапазона")

    def _count_type(self, target_type: type) -> int:
        count = 0
        for row in self._grid:
            for cell in row:
                if cell.unit and type(cell.unit) is target_type:
                    count += 1
        return count

    def copy(self) -> "FieldCells":
        return copy.deepcopy(self)

    def __str__(self) -> str:
        lines = []
        for row in self._grid:
            line = "X" + "".join(str(cell) for cell in row) + "X"
            lines.append(line)
        return "\n".join(lines)