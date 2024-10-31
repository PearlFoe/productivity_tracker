from dependency_injector import providers, containers


class CalendarContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.calendars.routers",
        ],
    )

    env = providers.Configuration()
