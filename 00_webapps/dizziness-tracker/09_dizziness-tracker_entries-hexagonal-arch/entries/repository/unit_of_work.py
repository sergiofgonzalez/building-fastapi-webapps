"""Transaction Management using the Unit of Work Design Pattern."""

from types import TracebackType

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class UnitOfWork:
    """Unit of Work design pattern using a SQLAlchemy session."""

    def __init__(self) -> None:
        """Initialize the unit of work."""
        self.session_maker = sessionmaker(
            bind=create_engine("sqlite:///entries.db"),
        )

    def __enter__(self) -> "UnitOfWork":
        """Carry out initialization actions on the unit of work."""
        self.session = self.session_maker()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Carry out clean up actions upon exiting the unit of work."""
        if exc_type is not None:
            self.rollback()
            self.session.close()
        self.session.close()

    def commit(self) -> None:
        """Commit all the in-flight changes to the database."""
        self.session.commit()

    def rollback(self) -> None:
        """Rollback any in-flight changes."""
        self.session.rollback()
