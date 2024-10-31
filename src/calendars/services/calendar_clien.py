from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from ..models.calendars import Calendar
from ..models.calendar_client.calendars import Calendar as APIData


class CalendarAPIClient:
    def __init__(
        self, service_account_creds: dict, api_name: str = "calendar", api_version: str = "v3"
    ) -> None:
        self._raw_creds = service_account_creds
        self._api_name = api_name
        self._api_version = api_version

    def _parse_creds(self, raw_creds: dict) -> ServiceAccountCreds:
        return ServiceAccountCreds(
            scopes=["https://www.googleapis.com/auth/calendar"],
            **raw_creds,
        )

    async def _request_calendar_info(self, calendar_id: str) -> APIData:
        creds = self._parse_creds(self._raw_creds)
        async with Aiogoogle(service_account_creds=creds) as aiogoogle:
            api = await aiogoogle.discover(self._api_name, self._api_version)
            calendar = await aiogoogle.as_service_account(
                api.calendars.get(calendar_id=calendar_id),
            )

        return APIData.model_validate(calendar)

    async def calendar_info(self, calendar_id: str) -> Calendar:
        api_data = await self._request_calendar_info(calendar_id)
        return Calendar(
            google_id=api_data.id,
            name=api_data.summary,
            timezone=api_data.timezone,
            primary=api_data.primary,
        )
