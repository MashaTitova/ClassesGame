from Objects.Landscape import Landscape
from Objects.Unit import Unit
class Forest(Landscape):
    """Лес — замедляет конницу, даёт защиту."""
    @property
    def icon(self) -> str:
        return "🌳"

    @property
    def name(self) -> str:
        return "Лес"

    def can_enter(self, unit: Unit) -> bool:
        return True

    def apply_effect(self, unit: Unit) -> None:
        if isinstance(unit, Cavalry):
            unit.take_damage(5)
