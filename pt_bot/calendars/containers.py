from os import path

from dependency_injector import containers, providers

from pt_bot.core.db.utils import init_db_connection_pool, load_queries

from .db.queries.builders import CalendarQueryBuilder
from .db.repositories import CalendarRepository
from .services.calendars import CalendarService
from .services.cliens import GoogleCalendarAPIClient


class CalendarContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "pt_bot.calendars.routers",
        ],
    )

    env = providers.Configuration()

    calendar_unloaded_qb = providers.Singleton(CalendarQueryBuilder)

    _calendar_queries_path = providers.Callable(
        path.join, env.project_dir, "pt_bot/calendars/db/queries/sql/calendar.sql"
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
        pool=pool,
        queries=calendar_qb,
    )

    google_calendar_client = providers.Factory(
        GoogleCalendarAPIClient,
        service_account_creds=env.google_client_secrets,
    )

    calendar_service = providers.Factory(
        CalendarService,
        calendar_repository=calendar_repository,
        client=google_calendar_client,
    )
