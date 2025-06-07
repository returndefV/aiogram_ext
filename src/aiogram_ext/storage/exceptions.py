class SqliteDatabaseCreationError(Exception):
    """Exception occurs when there is an error creating tables."""

class SqliteDatabaseDropError(Exception):
    """Exception occurs when database reset error occurs."""

class SqliteSessionError(Exception):
    """Exception occurs when there is an error in the database session."""
