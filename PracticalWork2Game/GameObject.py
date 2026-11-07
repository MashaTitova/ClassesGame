from abc import ABC, abstractmethod

class GameObject(ABC):
    @property
    @abstractmethod
    def icon(self) -> str:
        pass

    @property
    @abstractmethod
    def percent_on_field(self) -> int:
        pass
