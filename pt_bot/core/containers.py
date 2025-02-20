from os import path

from aiogram.fsm.storage.redis import RedisStorage
from dependency_injector import containers, providers

from pt_bot.core.db.utils import init_db_connection_pool, load_queries, redis_pool, redis_session

from .db.queries.builders import UserQueryBuilder
from .db.repositories import UserCacheRepository, UserRepository


class CoreContainer(containers.DeclarativeContainer):
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

    user_cache_repository = providers.Factory(
        UserCacheRepository,
        pool=redis_pool,
        ttl=env.user_data_ttl,
    )

    user_unloaded_qb = providers.Singleton(UserQueryBuilder)

    _user_queries_path = providers.Callable(path.join, env.project_dir, "pt_bot/bot/db/queries/sql/user.sql")
    user_qb = providers.Callable(
        load_queries,
        builder=user_unloaded_qb,
        path=_user_queries_path,
    )

    db_pool = providers.Resource(
        init_db_connection_pool,
        dsn=env.db_dsn,
    )

    user_repository = providers.Factory(
        UserRepository,
        pool=db_pool,
    )
