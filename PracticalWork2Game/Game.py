import random

import Field
from Objects.Base import Base
from Objects.Unit import Unit
from Objects.Landscapes.Plain import Plain
from Objects.Landscapes.Forest import Forest
from Objects.Landscapes.Mountain import Mountain
from Objects.NeutralObjects.Treasure import Treasure
from Objects.NeutralObjects.MagicRiver import MagicRiver
from Objects.NeutralObjects.Trap import Trap
from Objects.NeutralObjects.Obstacle import Obstacle
from Objects.Units.Infantries.Swordsman import Swordsman
from Objects.Units.Infantries.Spearman import Spearman
from Objects.Units.Archers.Bowman import Bowman
from Objects.Units.Archers.Crossbowman import Crossbowman
from Objects.Units.Cavalries.Knight import Knight
from Objects.Units.Cavalries.Lancer import Lancer

from UserProfile import UserProfile, ProfileStorage


class Game:
    def __init__(self, profile: UserProfile, width: int = 10, height: int = 10):
        self.profile = profile
        self.storage = ProfileStorage()

        self.field = Field.Field(width, height, max_capacity=50)
        self.base = Base(
            "Главная база",
            max_health=random.randint(300, 800),
            max_units=random.randint(5, 15),
        )

        self._history: list[tuple] = []
        self._setup_map()
        self.field.place_base(0, 0, self.base)


    def award(self, points: int, reason: str = "") -> None:
        """Начисление очков с учётом премиума."""
        real = int(points * (1.25 if self.profile.is_premium else 1.0))
        self.profile.add_score(real)
        print(f"🏆 +{real} очков {('— ' + reason) if reason else ''} "
              f"(всего: {self.profile.score})")

    def _checkpoint(self) -> None:
        self._history.append((self.field.copy(), self.profile.score))

    def _show_profile(self) -> None:
        print("\n--- 👤 Профиль ---")
        print(self.profile)
        print("[1] ⭐ Получить премиум (1000 очков)")
        print("[2] 💾 Сохранить профиль")
        print("[0] Назад")

        choice = input("Выбор: ").strip()
        if choice == "1":
            self.profile.upgrade_to_premium()
            self.storage.save(self.profile)
        elif choice == "2":
            self.storage.save(self.profile)
            print("✅ Профиль сохранён")


    def _setup_map(self) -> None:
        width, height = self.field.width, self.field.height

        for _ in range(random.randint(8, 15)):
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            if (x, y) == (0, 0):
                continue
            self.field.set_landscape(
                x, y, random.choice([Plain, Forest, Mountain])()
            )

        neutral_classes = [Treasure, MagicRiver, Trap, Obstacle]
        placed = attempts = 0
        while placed < random.randint(6, 12) and attempts < 100:
            attempts += 1
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            if (x, y) == (0, 0):
                continue
            cell = self.field.get_cell(x, y)
            if cell.neutral or cell.unit:
                continue
            cls = random.choice(neutral_classes)
            try:
                obj = Obstacle(durability=random.randint(30, 80)) \
                    if cls is Obstacle else cls()
                self.field.place_neutral(x, y, obj)
                placed += 1
            except ValueError:
                continue

    def _find_spawn(self) -> tuple[int, int] | None:
        cells = [
            (x, y)
            for x in range(self.field.width)
            for y in range(self.field.height)
            if (x, y) != (0, 0) and self.field.get_cell(x, y).unit is None
        ]
        random.shuffle(cells)
        cells.sort(key=lambda p: max(p))
        return cells[0] if cells else None


    def run(self) -> None:
        print(f"\n🎮 Игра началась! Игрок: {self.profile.username}")
        print(f"🏰 База: HP={self.base.health}, макс. юнитов={self.base.max_units}")

        while True:
            print("\n" + "=" * 40)
            print(self.field)
            print(f"\n{self.base}")
            print(f"👤 {self.profile.username} | 🏆 {self.profile.score} очков")
            print(f"📊 Ходов сделано: {len(self._history)}")

            print("\n[1] 🏰 Управление базой (создать юнита)")
            print("[2] ⚔️  Управление юнитом")
            print("[3] 📋 Состояние базы")
            print("[4] ↩️  Отменить последний ход")
            print("[5] 💾 Сохранить игру (поле + профиль)")
            print("[6] 👤 Профиль / премиум")
            print("[0] 🚪 Выход")

            choice = input("\nВыберите действие: ").strip()

            if choice == "1":
                self._base_menu()
            elif choice == "2":
                self._unit_menu()
            elif choice == "3":
                self._show_base_status()
            elif choice == "4":
                self._undo_last_move()
            elif choice == "5":
                self._save_field_state()
            elif choice == "6":
                self._show_profile()
            elif choice == "0":
                self.storage.save(self.profile)
                print(f"💾 Профиль {self.profile.username} сохранён. Пока!")
                break
            else:
                print("❌ Неверный выбор")

    def _base_menu(self) -> None:
        print("\n--- 🏰 Управление базой ---")
        classes = {
            "1": ("⚔️ Мечник", Swordsman),
            "2": ("🔱 Копейщик", Spearman),
            "3": ("🏹 Лучник", Bowman),
            "4": ("🎯 Арбалетчик", Crossbowman),
            "5": ("🐴 Рыцарь", Knight),
            "6": ("🏇 Лансер", Lancer),
        }
        for key, (name, _) in classes.items():
            print(f"[{key}] {name}")
        print("[0] Назад")

        choice = input("Выбор: ").strip()
        if choice not in classes:
            return

        spawn = self._find_spawn()
        if spawn is None:
            print("❌ Нет свободного места вокруг базы")
            return

        try:
            unit = self.base.create_unit(classes[choice][1])
        except ValueError as e:
            print(f"❌ {e}")
            return

        x, y = spawn
        try:
            self.field.place_unit(x, y, unit)
            print(f"✅ {unit.name} создан на ({x}, {y})")
            self.award(10, "создание юнита")
        except ValueError as e:
            print(f"❌ Не удалось разместить юнита: {e}")


    def _unit_menu(self) -> None:
        alive = [u for u in self.base.units if u.is_alive]
        if not alive:
            print("❌ Нет живых юнитов")
            return

        print("\n--- ⚔️ Ваши юниты ---")
        for i, unit in enumerate(alive, 1):
            print(f"[{i}] {unit} на {unit.position} | {repr(unit)}")

        try:
            idx = int(input("Выберите юнита (0 — назад): ")) - 1
            if idx < 0:
                return
            self._control_unit(alive[idx])
        except (ValueError, IndexError):
            print("❌ Неверный выбор")

    def _control_unit(self, unit: Unit) -> None:
        while unit.is_alive:
            print(f"\n{unit} на {unit.position}")
            print("[1] 🏃 Двигаться\n[2] ⚔️ Атаковать\n"
                  "[3] 🤝 Взаимодействовать\n[4] 💊 Лечиться\n[0] Назад")

            choice = input("Действие: ").strip()
            if choice == "1":
                self._move_unit(unit)
            elif choice == "2":
                self._attack_with_unit(unit)
            elif choice == "3":
                self._interact_with_object(unit)
            elif choice == "4":
                self._heal_unit(unit)
            elif choice == "0":
                break

    def _move_unit(self, unit: Unit) -> None:
        try:
            dx = int(input("ΔX: "))
            dy = int(input("ΔY: "))
            x, y = unit.position
            nx, ny = x + dx, y + dy

            if not (0 <= nx < self.field.width and 0 <= ny < self.field.height):
                print("❌ Выход за границы поля")
                return

            cell = self.field.get_cell(nx, ny)
            if not cell.is_passable(unit):
                print(f"❌ Клетка непроходима: {cell.landscape.name}")
                return

            self._checkpoint()
            self.field.remove_unit(x, y)
            unit.move(dx, dy, cell.landscape)
            self.field.place_unit(nx, ny, unit)

            print(f"✅ {unit.name} → ({nx}, {ny}), {cell.landscape.name}")
            self.award(5, "перемещение")

            if cell.neutral:
                self._interact_with_object(unit, save_state=False)

        except (ValueError, IndexError) as e:
            print(f"❌ Ошибка: {e}")

    def _attack_with_unit(self, unit: Unit) -> None:
        radius = unit.get_attack_range()
        targets = [
            t for t in self.base.units
            if t.is_alive and t != unit
            and max(abs(unit.position[0] - t.position[0]),
                    abs(unit.position[1] - t.position[1])) <= radius
        ]

        if not targets:
            print(f"❌ Нет целей в радиусе {radius}")
            return

        print(f"\n--- Цели в радиусе {radius} ---")
        for i, target in enumerate(targets, 1):
            print(f"[{i}] {target} на {target.position}")

        try:
            choice = int(input("Цель (0 — отмена): "))
            if not 1 <= choice <= len(targets):
                return
            target = targets[choice - 1]   # исправлено: прежний индекс считался по всем юнитам
        except ValueError:
            print("❌ Неверный выбор")
            return

        self._checkpoint()
        unit.attack_unit(target)
        self.award(10, "атака")
        print(f"⚔️ {target.name}: HP={target.health}")

        if not target.is_alive:
            tx, ty = target.position
            self.field.remove_unit(tx, ty)
            self.base.on_unit_destroyed(target)
            self.award(50, "уничтожение врага")
            print(f"💀 {target.name} уничтожен")

    def _interact_with_object(self, unit: Unit, save_state: bool = True) -> None:
        x, y = unit.position
        cell = self.field.get_cell(x, y)
        if not cell.neutral:
            print("❌ Здесь не с чем взаимодействовать")
            return

        if save_state:
            self._checkpoint()

        print(f"🎯 Взаимодействие с {cell.neutral.icon}")
        result = unit + cell.neutral
        if result == "destroyed":
            self.field.remove_neutral(x, y)
            self.award(15, "разрушение объекта")
            print("💥 Объект разрушен")

    def _heal_unit(self, unit: Unit) -> None:
        cost = 5 if self.profile.is_premium else 10
        amount = 20
        gold = getattr(unit, "_gold", 0)

        print(f"💊 +{amount} HP за {cost} золота | у вас: {gold}")
        if input("Лечиться? (д/н): ").strip().lower() != "д":
            return
        if gold < cost:
            print("❌ Недостаточно золота")
            return

        self._checkpoint()
        unit._gold = gold - cost
        unit.heal(amount)
        print(f"✅ {unit.name} восстановил {amount} HP")


    def _undo_last_move(self) -> None:
        if not self._history:
            print("❌ Нечего отменять")
            return
        snapshot, score = self._history.pop()
        self.field = snapshot
        self.profile.score = score
        print("✅ Ход и очки восстановлены")

    def _save_field_state(self) -> None:
        self._checkpoint()
        self.storage.save(self.profile)
        print(f"💾 Снимок поля сохранён, профиль записан "
              f"(снимков: {len(self._history)})")

    def _show_base_status(self) -> None:
        print("\n" + "=" * 40)
        print(f"🏰 {self.base.name}")
        print(f"❤️ HP: {self.base.health}/{self.base._max_health}")
        print(f"👥 Юнитов: {self.base.alive_units_count}/{self.base.max_units}")
        print("Список юнитов:")
        for unit in self.base.units:
            status = "✅ жив" if unit.is_alive else "💀 мёртв"
            print(f"  • {unit} [{status}] на {unit.position} "
                  f"| 💰 {getattr(unit, '_gold', 0)}")
            print(f"    {repr(unit)}")



def authorize(storage: ProfileStorage) -> UserProfile | None:
    while True:
        print("\n" + "=" * 40)
        print("👤 ВХОД В ИГРУ")
        print("[1] Регистрация")
        print("[2] Вход")
        print("[0] Выход")

        choice = input("Выбор: ").strip()

        if choice == "1":
            try:
                username = input("Логин (3–20, латиница/цифры/_): ").strip()
                email = input("Email: ").strip()
                age = int(input("Возраст: ").strip())
                return storage.register(username, email, age)
            except (ValueError, TypeError) as e:
                print(f"❌ {e}")

        elif choice == "2":
            users = storage.usernames()
            print(f"Известные профили: {', '.join(users) or 'нет'}")
            try:
                return storage.login(input("Логин: ").strip())
            except (ValueError, KeyError, OSError) as e:
                print(f"❌ {e}")

        elif choice == "0":
            return None


if __name__ == "__main__":
    storage = ProfileStorage()
    profile = authorize(storage)
    if profile is not None:
        Game(profile, width=10, height=10).run()