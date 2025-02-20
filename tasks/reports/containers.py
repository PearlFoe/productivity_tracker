from concurrent.futures import ThreadPoolExecutor
from os import path

from aiogram import Bot
from dependency_injector import containers, providers

from tasks.core.db.utils import init_db_connection_pool, load_queries

from .db.queries.reports import ReportQueryBuilder
from .db.queries.user import UserQueryBuilder
from .db.repositories.reports import ReportRepository
from .db.repositories.user import UserRepository
from .services.distribution import ReportDistributionService
from .services.report_builders import ReportBuildingService


class ReportContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        auto_wire=False,
        modules=[],
    )

    env = providers.Configuration()

    report_unloaded_qb = providers.Singleton(ReportQueryBuilder)

    _report_queries_path = providers.Callable(
        path.join,
        env.project_dir,
        "tasks/reports/db/queries/sql/report.sql",
    )

    report_qb = providers.Factory(
        load_queries,
        builder=report_unloaded_qb,
        path=_report_queries_path,
    )

    db_connection_pool = providers.Resource(
        init_db_connection_pool,
        dsn=env.db_dsn,
    )

    report_repository = providers.Factory(
        ReportRepository,
        pool=db_connection_pool,
        queries=report_qb,
    )

    thread_pool = providers.Factory(
        ThreadPoolExecutor,
    )

    report_building_service = providers.Factory(
        ReportBuildingService,
        statistics=report_repository,
        pool=thread_pool,
    )

    user_unloaded_qb = providers.Singleton(UserQueryBuilder)

    _user_queries_path = providers.Callable(
        path.join,
        env.project_dir,
        "tasks/reports/db/queries/sql/user.sql",
    )

    user_qb = providers.Factory(
        load_queries,
        builder=user_unloaded_qb,
        path=_user_queries_path,
    )

    bot = providers.Factory(
        Bot,
        token=env.bot_api_token,
    )

    user_repository = providers.Factory(
        UserRepository,
        pool=db_connection_pool,
        queries=user_qb,
    )

    report_distribution_service = providers.Factory(
        ReportDistributionService,
        bot=bot,
        user=user_repository,
        report=report_repository,
    )
