from dependency_injector import containers, providers
from aiogram.fsm.storage.redis import RedisStorage

from .utils import redis_pool, redis_session


class BotContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[],
    )

    env = providers.Configuration()

    redis_connection_pool = providers.Resource(
        redis_pool,
        redis_dsn=env.redis_dsn,
    )

    redis_session = providers.Resource(
        redis_session,
        pool=redis_connection_pool,
    )

    redis_storage = providers.Factory(
        RedisStorage,
        redis=redis_session,
    )
