from dependency_injector import containers, providers

from .services.report_builders import ReportBuildingService


class ReportContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        auto_wire=False,
        modules=[],
    )

    env = providers.Configuration()

    report_building_service = providers.Factory(
        ReportBuildingService,
    )
