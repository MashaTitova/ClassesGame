from Objects.Units.Archer import Archer
from Objects.Unit import Unit
class Crossbowman(Archer):
    def __init__(self):
        super().__init__("Арбалетчик", 10, "🎯", 60, 3, 25, 4)

    def attack_unit(self, target: Unit) -> None:
        damage = max(0, self.attack - target.armor // 2)
        target._health = max(0, target._health - damage)
        print(f"{self.name} стреляет в {target.name} (пробивает броню)")