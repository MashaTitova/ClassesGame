from Objects.Units.Cavalry import Cavalry
from Objects.Units.Infantry import Infantry
from Objects.Unit import Unit
class Lancer(Cavalry):
    def __init__(self):
        super().__init__("Лансьер", 8, "🏇", 100, 12, 22)

    def attack_unit(self, target: Unit) -> None:
        damage = self.attack
        if isinstance(target, Infantry):
            damage = int(damage * 1.3)
        target.take_damage(damage)
        print(f"{self.name} атакует {target.name}")