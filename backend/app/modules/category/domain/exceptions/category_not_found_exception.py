from uuid import UUID
from app.common.exceptions import NotFoundException

class CategoryNotFoundException(NotFoundException):
    """
    Exception raised when a category is not found.
    """
    def __init__(self, category_id: UUID):
        super().__init__(
            message=f"Category with id '{category_id}' was not found.",
            code="CATEGORY_NOT_FOUND",
            details={
                "category_id": str(category_id)
            }
        )
