from os import path

from dependency_injector import containers, providers

from tasks.core.db.utils import init_db_connection_pool, load_queries

from .db.queries.builders import CalendarQueryBuilder
from .db.repositories import CalendarRepository
from .services.calendars import CalendarService
from .services.clients import GoogleCalendarAPIClient
from .services.statistics import StatisticsService


class CalendarsStatisticsContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        auto_wire=False,
        modules=[
            "tasks.calendars_statistics.flows",
        ],
    )

    env = providers.Configuration()

    calendar_unloaded_qb = providers.Singleton(CalendarQueryBuilder)

    _calendar_queries_path = providers.Callable(
        path.join, env.project_dir, "tasks/calendars_statistics/db/queries/sql/calendar.sql"
    )
    calendar_qb = providers.Callable(
        load_queries,
        builder=calendar_unloaded_qb,
        path=_calendar_queries_path,
    )

    pool = providers.Resource(
        init_db_connection_pool,
        dsn=env.db_dsn,
    )

    calendar_repository = providers.Factory(
        CalendarRepository,
    )

    calendar_service = providers.Factory(
        CalendarService,
        calendar_repository=calendar_repository,
    )

    google_api_client = providers.Factory(
        GoogleCalendarAPIClient,
        service_account_creds=env.google_client_secrets,
    )

    statistics_service = providers.Factory(
        StatisticsService,
    )
