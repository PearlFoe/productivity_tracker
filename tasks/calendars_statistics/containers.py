from dependency_injector import containers, providers


class CalendarsStatisticsContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "tasks.calendars_statistics.flows",
        ],
    )

    env = providers.Configuration()
