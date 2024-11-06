from enum import StrEnum


class CalendarMessages(StrEnum):
    REQUEST_LINK = "Send link to the calendar you want to analyze"
    CHOOSE_CATEGORY = "Coose calendars category"
    CALENDAR_ADDED_SUCCESSFULLY = "Calendar added successfully"
    INVALID_CALENDAR_LINK = "Invalid link or access to the calendar was not granted"
    CALENDAR_DUPLICATE = "You have already added this calendar before"
