from Objects.Units.Infantry import Infantry
from Objects.Units.Cavalry import Cavalry
from Objects.Unit import Unit
class Spearman(Infantry):
    def __init__(self):
        super().__init__("Копейщик", 20, "🔱", 90, 15, 12)

    def attack_unit(self, target: Unit) -> None:
        damage = self.attack
        if isinstance(target, Cavalry):
            damage = int(damage * 1.5)
        target.take_damage(damage)
        print(f"{self.name} атакует {target.name} на {damage}")