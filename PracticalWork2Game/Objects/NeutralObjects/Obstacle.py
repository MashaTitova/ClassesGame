from Objects.NeutralObject import NeutralObject
from Objects.Unit import Unit

class Obstacle(NeutralObject):
    """Препятствие - можно разрушить."""
    @property
    def icon(self) -> str:
        return "🪵"

    @property
    def percent_on_field(self) -> int:
        return 15

    def __init__(self, durability: int = 50):
        self.durability = durability

    def interact(self, unit: Unit) -> Unit:
        self.durability -= unit.attack
        if self.durability <= 0:
            print(f"💥 {unit.name} разрушил препятствие!")
            return "destroyed"
        print(f"🪵 {unit.name} бьёт препятствие. Осталось: {self.durability} HP")
        return unit