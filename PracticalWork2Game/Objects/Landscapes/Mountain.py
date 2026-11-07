from Objects.Landscape import Landscape
from Objects.Unit import Unit
class Mountain(Landscape):
    """Горы - непроходимы для конницы."""
    @property
    def icon(self) -> str:
        return "🏔️"

    @property
    def name(self) -> str:
        return "Горы"

    def can_enter(self, unit: Unit) -> bool:
        from Objects.Units.Cavalry import Cavalry
        return not isinstance(unit, Cavalry)

    def apply_effect(self, unit: Unit) -> None:
        pass