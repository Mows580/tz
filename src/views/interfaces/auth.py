from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class AuthInterface(ABC):
    @abstractmethod
    async def login(self, payload, session:AsyncSession):...
    @abstractmethod
    async def registration(self, payload, session:AsyncSession):...