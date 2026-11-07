from Objects.Units.Archer import Archer
from Objects.Unit import Unit
class Bowman(Archer):
    def __init__(self):
        super().__init__("Лучник", 15, "🏹", 70, 5, 18, 3)

    def attack_unit(self, target: Unit) -> None:
        target.take_damage(self.attack)
        print(f"{self.name} стреляет в {target.name}")