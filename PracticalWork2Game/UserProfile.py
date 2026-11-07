import json
import re
from datetime import datetime
from pathlib import Path


class UserProfile:
    def __init__(self, username: str, email: str, age: int):
        self.username = username
        self.email = email
        self.age = age
        self._score = 0
        self._created_at = datetime.now().isoformat()
        self._is_premium = False

    @property
    def username(self) -> str:
        return self._username

    @property
    def created_at(self) -> str:
        return self._created_at

    @username.setter
    def username(self, value: str) -> None:
        if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_]{3,20}", value):
            raise ValueError("Логин: 3–20 символов, латиница, цифры, _")
        self._username = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            raise ValueError(f"Некорректный email: {value}")
        self._email = value

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("Возраст должен быть целым числом")
        if not 0 < value <= 100:
            raise ValueError("Возраст должен быть от 1 до 100")
        self._age = value

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("Очки должны быть целым числом")
        if value < 0:
            raise ValueError("Очки не могут быть отрицательными")
        self._score = value

    @property
    def is_premium(self) -> bool:
        return self._is_premium

    @is_premium.setter
    def is_premium(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("is_premium должен быть bool")
        self._is_premium = value

    def add_score(self, points: int) -> None:
        self.score = self._score + points

    def upgrade_to_premium(self) -> bool:
        if self._score >= 1000:
            self.is_premium = True
            print(f"⭐ {self._username} получил премиум-статус!")
            return True
        print(f"❌ Нужно 1000 очков, есть {self._score}")
        return False

    def to_dict(self) -> dict:
        return {
            "username": self._username,
            "email": self._email,
            "age": self._age,
            "score": self._score,
            "created_at": self._created_at,
            "is_premium": self._is_premium,   # было потеряно
        }

    def save_to_json(self, filepath: str) -> None:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4, ensure_ascii=False)

    @classmethod
    def load_from_json(cls, filepath: str) -> "UserProfile":
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        profile = cls(data["username"], data["email"], data["age"])
        profile.score = data.get("score", 0)
        profile._created_at = data.get("created_at", datetime.now().isoformat())
        profile.is_premium = data.get("is_premium", False)
        return profile

    def __str__(self) -> str:
        status = "⭐ Премиум" if self._is_premium else "Обычный"
        return (
            f"👤 {self._username} ({status})\n"
            f"   Email: {self._email}\n"
            f"   Возраст: {self._age}\n"
            f"   Очки: {self._score}\n"
            f"   Создан: {self._created_at}"
        )

    def __repr__(self) -> str:
        return (
            f"UserProfile(username='{self._username}', email='{self._email}', "
            f"age={self._age}, score={self._score})"
        )


class ProfileStorage:
    """Регистрация / вход / сохранение профилей на диске."""

    def __init__(self, directory: str = "profiles"):
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)

    def _path(self, username: str) -> Path:
        return self.dir / f"{username}.json"

    def exists(self, username: str) -> bool:
        return self._path(username).exists()

    def register(self, username: str, email: str, age: int) -> UserProfile:
        if self.exists(username):
            raise ValueError(f"Пользователь '{username}' уже зарегистрирован")
        profile = UserProfile(username, email, age)
        profile.save_to_json(str(self._path(username)))
        print(f"✅ Аккаунт '{username}' создан")
        return profile

    def login(self, username: str) -> UserProfile:
        if not self.exists(username):
            raise ValueError(f"Пользователь '{username}' не найден")
        profile = UserProfile.load_from_json(str(self._path(username)))
        print(f"✅ С возвращением, {profile.username}!")
        return profile

    def save(self, profile: UserProfile) -> None:
        profile.save_to_json(str(self._path(profile.username)))

    def usernames(self) -> list[str]:
        return [p.stem for p in self.dir.glob("*.json")]