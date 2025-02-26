import json
from datetime import datetime

from aiogoogle import Aiogoogle, excs
from aiogoogle.auth.creds import ServiceAccountCreds
from prefect.logging import get_run_logger
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

from ..constants import GOOGLE_API_DATETIME_FORMAT
from ..models.client.events import Event


class GoogleCalendarAPIClient:
    def __init__(
        self, service_account_creds: str, api_name: str = "calendar", api_version: str = "v3"
    ) -> None:
        self._raw_creds = service_account_creds
        self._api_name = api_name
        self._api_version = api_version

    def _parse_creds(self, raw_creds: str) -> ServiceAccountCreds:
        return ServiceAccountCreds(
            scopes=["https://www.googleapis.com/auth/calendar"],
            **json.loads(raw_creds),
        )

    @staticmethod
    def _format_datetime(d: datetime) -> str:
        return d.strftime(GOOGLE_API_DATETIME_FORMAT)

    async def _request_events_info(self, calendar_id: str, start: datetime, end: datetime) -> list[Event]:
        creds = self._parse_creds(self._raw_creds)
        async with Aiogoogle(service_account_creds=creds) as aiogoogle:
            api = await aiogoogle.discover(self._api_name, self._api_version)
            response = await aiogoogle.as_service_account(
                api.events.list(
                    calendarId=calendar_id,
                    timeMin=self._format_datetime(start),
                    timeMax=self._format_datetime(end),
                    singleEvents=True,
                    orderBy="startTime",
                )
            )
            return [Event.model_validate(event) for event in response["items"]]

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential_jitter(
            initial=1,
            max=60,
        ),
        retry=retry_if_exception_type(excs.HTTPError),
    )
    async def events(self, calendar_id: str, start: datetime, end: datetime) -> list[Event]:
        logger = get_run_logger()
        try:
            return await self._request_events_info(calendar_id, start, end)
        except excs.HTTPError as e:
            logger.warning(e, exc_info=True)
            match e.res.status_code:
                case code if code in (408, 429):
                    raise e
                case code if code >= 500:
                    raise e
                case _:
                    return []
        except excs.AiogoogleError as e:
            logger.exception(e)
            return []
