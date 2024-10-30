from enum import StrEnum


class StartMessages(StrEnum):
    START = "Hello, this is your personal productivity tracker. PT " \
            "can help you to track your activity and give personalized " \
            "recommendation based on events from your calendars."
    NEW_CALLENDAR = "Let's connect /calendar to your account "\
                    "(you can change them later at any time)."
