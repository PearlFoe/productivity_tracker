from concurrent.futures import ThreadPoolExecutor
from os import path

from dependency_injector import containers, providers

from tasks.core.db.utils import init_db_connection_pool, load_queries

from .db.queries.builders import ReportQueryBuilder
from .db.repositories import ReportRepository
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
