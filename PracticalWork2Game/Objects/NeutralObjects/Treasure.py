from Objects.NeutralObject import NeutralObject
from Objects.Unit import Unit
class Treasure(NeutralObject):
    """Сокровище - даёт золото."""
    @property
    def icon(self) -> str:
        return "💰"

    @property
    def percent_on_field(self) -> int:
        return 15

    def interact(self, unit: Unit) -> Unit:
        unit._gold += 50
        print(f"💰 {unit.name} нашёл 50 золота! Всего: {unit._gold}")
        return unit