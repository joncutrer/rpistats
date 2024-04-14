# Publisher base class
from abc import ABC, abstractmethod


class Publisher(ABC):
    @abstractmethod
    def publish(self, data):
        pass
