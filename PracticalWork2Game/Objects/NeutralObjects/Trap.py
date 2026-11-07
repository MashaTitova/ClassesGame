from Objects.NeutralObject import NeutralObject
from Objects.Unit import Unit
class Trap(NeutralObject):
    """Ловушка - наносит урон"""
    @property
    def icon(self) -> str:
        return "💣"

    @property
    def percent_on_field(self) -> int:
        return 10

    def interact(self, unit: Unit) -> Unit:
        damage = unit.take_damage(25)
        print(f"💣 {unit.name} попал в ловушку! Урон: {damage}")
        return unit