class DatabaseAlreadyExists(Exception):
    """Raised by trying init new database when it exists"""
    def __init__(self, db_path):
        self.message = f"Database `{db_path}` already exists"
        super().__init__(self.message)
