from abc import ABC, abstractmethod
from app.schemas.module_output import ModuleOutput


class AuditModule(ABC):
    @abstractmethod
    def run(self, *args, **kwargs) -> ModuleOutput:
        """
        Run the audit and return the standard output contract.
        """
        raise NotImplementedError