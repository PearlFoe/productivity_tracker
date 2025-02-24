from enum import StrEnum


class CalendarMessages(StrEnum):
    MENU = "Choose the action you want to do"
    REQUEST_LINK = "Send link to the calendar you want to analyze"
    CHOOSE_CATEGORY = "Coose calendars category"
    CHOOSE_NAME = "Choose calendar to disable"
    СALENDAR_DISABLED_SUCCESSFULLY = "Calendar disabled successfully"
    CALENDAR_ADDED_SUCCESSFULLY = "Calendar added successfully"
    INVALID_CALENDAR_LINK = "Invalid link or access to the calendar was not granted"
    CALENDAR_DUPLICATE = "You have already added this calendar before"
