class CompanyAlreadyExistsException(Exception):
    """Exception raised when trying to register a company that already exists."""
    def __init__(self, message: str = "Company already exists"):
        self.message = message
        super().__init__(self.message)
