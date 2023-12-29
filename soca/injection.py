from functools import lru_cache

from config.settings import Settings


@lru_cache
def settings():
    return Settings()
