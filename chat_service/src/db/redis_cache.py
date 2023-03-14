import hashlib
import logging
from typing import Optional

# from aioredis import Redis
from redis.asyncio import Redis

# переменная хранит объект подключения после чего передачи
redis_conn: Optional[Redis] = None


async def get_cache_conn() -> Optional[Redis]:
    """Вернуть подключение к redis, если оно создано, иначе None."""
    return redis_conn


class Redis:
    """Реализация интерфейса кэша и работающая через redis."""

    def __init__(self, redis_conn: Redis):
        self.redis: Redis = redis_conn

    async def get_cache(self, key: str) -> Optional[bytes]:
        """Получить запись из кэша по переданному ключу.
        Args:
            key: ключ
        Returns:
            Запись из кэша в формате bytes.
        """
        data = await self.redis.get(key)
        return data

    async def set_cache(self, key: str, data: bytes, expire: int = 60 * 60 * 5) -> None:
        """Создать запись в Redis по переданному ключу.
        Args:
            key: ключ, по которому будет создана запись.
            data: данные, которые будут записаны в кэш.
        Returns:
            None
        """
        await self.redis.set(key, data, ex=expire)
        logging.info("record in cache created.")

    async def create_key(
        self,
        params: list,
    ) -> str:
        """создать ключ для запроса.
        Args:
            params: поля запроса.
        Returns:
            str: ключ для данного запроса.
        """
        data = ",".join([str(param) for param in params])
        key = data.encode("utf-8")

        return hashlib.md5(key).hexdigest()
