from Objects.Landscape import Landscape
from Objects.Unit import Unit
class Plain(Landscape):
    @property
    def icon(self) -> str:
        return "🟩"

    @property
    def name(self) -> str:
        return "Равнина"

    def can_enter(self, unit: Unit) -> bool:
        return True

    def apply_effect(self, unit: Unit) -> None:
        from Objects.Units.Cavalry import Cavalry
        from Objects.Units.Archer import Archer
        from Objects.Units.Infantry import Infantry
        # Конница получает бонус к атаке
        if isinstance(unit, Cavalry):
            unit.attack += 3
            print(f"💨 {unit.name} получает бонус +3 к атаке на равнине")

        # Лучники получают бонус к дальности
        elif isinstance(unit, Archer):
            unit._attack_range += 1
            print(f"👁️ {unit.name} получает бонус +1 к дальности на равнине")

        # Пехота получает минус к защите
        elif isinstance(unit, Infantry):
            unit.armor = max(0, unit.armor - 2)
            print(f"⚠️ {unit.name} теряет -2 к броне на открытой равнине")