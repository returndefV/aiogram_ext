class PostgresqlDatabaseCreationError(Exception):
    """Exception occurs when there is an error creating tables.."""

class PostgresqlDatabaseDropError(Exception):
    """Exception occurs when database reset error occurs."""
