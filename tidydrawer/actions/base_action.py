from abc import ABC, abstractmethod
from typing import Dict, Any


class Action(ABC):
    @abstractmethod
    def execute(self, file_data: Dict[str, Any]) -> str:
        """Execute the action on the given file."""
        pass