from abc import ABC, abstractmethod

# Define the Collector interface
class Collector(ABC):
    @abstractmethod
    def collect(self):
        """Collect statistics."""
        pass

