from Objects.NeutralObject import NeutralObject
from Objects.Unit import Unit
class MagicRiver(NeutralObject):
    """Волшебная река — лечит юнита."""
    @property
    def icon(self) -> str:
        return "🌊"

    @property
    def percent_on_field(self) -> int:
        return 10

    def interact(self, unit: Unit) -> Unit:
        unit.heal(30)
        print(f"🌊 {unit.name} восстановил 30 HP")
        return unit