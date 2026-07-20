from uuid import UUID

class CompanyNotFoundException(Exception):
    """Exception raised when a requested company is not found in the domain."""
    def __init__(self, company_id: UUID):
        self.company_id = company_id
        self.message = f"Company with id {company_id} not found"
        super().__init__(self.message)
