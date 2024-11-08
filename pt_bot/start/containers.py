from os import path

from dependency_injector import containers, providers

from pt_bot.core.db.utils import init_db_connection_pool, load_queries

from .db.queries.builders import UserQueryBuilder
from .db.repositories import UserRepository
from .services.users import UserService


class StartContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "pt_bot.start.routers",
        ],
    )

    env = providers.Configuration()

    user_unloaded_qb = providers.Singleton(UserQueryBuilder)

    _user_queries_path = providers.Callable(
        path.join, env.project_dir, "pt_bot/start/db/queries/sql/user.sql"
    )
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
