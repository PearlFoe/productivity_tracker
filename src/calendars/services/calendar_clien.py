from aiogoogle.auth.creds import ServiceAccountCreds


class CalendarClient:
    def __init__(self, service_account_creds: dict) -> None:
        self._raw_creds = service_account_creds

    def _parse_creds(self, raw_creds: dict) -> ServiceAccountCreds:
        return ServiceAccountCreds(
            scopes=["https://www.googleapis.com/auth/calendar"],
            **raw_creds,
        )
