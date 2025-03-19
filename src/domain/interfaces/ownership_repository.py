from abc import ABC, abstractmethod

from domain.models.ownership import Ownership


class OwnershipRepository(ABC):
    @abstractmethod
    def get_ownership_structure(
        self, focus_company: str
    ) -> tuple[list[Ownership], list[Ownership]]:
        pass
