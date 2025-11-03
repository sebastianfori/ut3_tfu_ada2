from contextlib import AbstractContextManager
from typing import Callable
from ..db import SessionLocal

class UnitOfWork(AbstractContextManager):
    """
    Unit of Work: centraliza manejo transaccional (commit/rollback) y entrega la session.
    """
    def __init__(self, session_factory: Callable = SessionLocal):
        self._session_factory = session_factory
        self.session = None

    def __enter__(self):
        self.session = self._session_factory()
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            if exc:
                self.session.rollback()
            else:
                self.session.commit()
        finally:
            self.session.close()
        return False
