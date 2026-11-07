from Objects.Units.Cavalry import Cavalry
from Objects.Unit import Unit
class Knight(Cavalry):
    def __init__(self):
        super().__init__("Рыцарь", 10, "🐴", 120, 20, 20)

    def attack_unit(self, target: Unit) -> None:
        target.take_damage(self.attack)
        print(f"{self.name} атакует {target.name}")