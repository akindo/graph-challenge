from domain.interfaces.ownership_repository import OwnershipRepository
from domain.models.ownership import Ownership
from infrastructure.utils.file_reader import (
    convert_to_ownership_objects,
    read_file,
)


class OwnershipRepository(OwnershipRepository):
    def get_ownership_structure(
        self, filepath: str
    ) -> tuple[list[Ownership], list[Ownership]]:
        """Reads JSON file, converts it to Ownership objects, and returns the list."""

        ownership_file_data = read_file(filepath)
        ownership_objects = convert_to_ownership_objects(ownership_file_data)

        owners_of_company = [
            item for item in ownership_objects if item.source_depth > 0
        ]
        companies_company_owns = [
            item for item in ownership_objects if item.source_depth <= 0
        ]

        return (owners_of_company, companies_company_owns)
