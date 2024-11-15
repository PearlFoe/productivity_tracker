from dependency_injector import containers, providers

from .services.statistics import StatisticsService


class CalendarsStatisticsContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        auto_wire=False,
        modules=[
            "tasks.calendars_statistics.flows",
        ],
    )

    env = providers.Configuration()

    statistics_service = providers.Factory(
        StatisticsService,
    )
