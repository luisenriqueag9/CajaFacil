class InvalidCompanyException(Exception):
    """Exception raised when company data or details are invalid."""
    def __init__(self, message: str = "Invalid company details"):
        self.message = message
        super().__init__(self.message)
