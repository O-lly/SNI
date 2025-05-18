# models/interfaces.py

from abc import ABC, abstractmethod
from models.entities import Post

class ContentFetcher(ABC):
    """Busca dados brutos de uma fonte externa."""
    source_name: str

    @abstractmethod
    async def fetch(self) -> list[dict]:
        pass

class ContentFormatter(ABC):
    """Converte dict cru em entidade Post."""
    source_name: str

    @abstractmethod
    def format(self, raw: dict) -> Post:
        pass

class ContentPublisher(ABC):
    """Publica uma entidade Post em um destino externo."""
    target_name: str

    @abstractmethod
    async def publish(self, post: Post) -> None:
        pass