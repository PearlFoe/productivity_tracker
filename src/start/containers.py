from os import path

from dependency_injector import containers, providers

from .db.repositories import UserRepository
from .db.queries.builders import UserQueryBuilder
from .db.utils import load_queries, init_db_connection_pool
from .services.users import UserService


class StartContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.start.routers",
        ],
    )

    env = providers.Configuration()

    user_unloaded_qb = providers.Singleton(
        UserQueryBuilder
    )

    user_qb = providers.Callable(
        load_queries,
        builder=user_unloaded_qb,
        path=path.join(env.project_dir, "src/start/db/queries/sql/user.sql"),
    )

    pool = providers.Singleton(
        init_db_connection_pool,
        dsn=env.db_dsn,
    )

    user_repository = providers.Factory(
        UserRepository,
        pool=pool,
        queries=user_qb,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )
