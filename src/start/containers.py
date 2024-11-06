from os import path

from dependency_injector import containers, providers

from src.core.db.utils import load_queries, init_db_connection_pool
from .db.repositories import UserRepository
from .db.queries.builders import UserQueryBuilder
from .services.users import UserService


class StartContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.start.routers",
        ],
    )

    env = providers.Configuration()

    user_unloaded_qb = providers.Singleton(UserQueryBuilder)

    _user_queries_path = providers.Callable(path.join, env.project_dir, "src/start/db/queries/sql/user.sql")
    user_qb = providers.Callable(
        load_queries,
        builder=user_unloaded_qb,
        path=_user_queries_path,
    )

    pool = providers.Resource(
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
