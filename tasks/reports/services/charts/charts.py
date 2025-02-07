from abc import ABC, abstractmethod
from collections.abc import Iterable
from enum import StrEnum, auto

from pygal import Graph

from tasks.reports.models.statistics import DailyStatistics

SVG = str


class ChartType(StrEnum):
    LINE = auto()
    STACKED_LINE = auto()
    PIE = auto()


class BaseChart(ABC):
    type: ChartType
    title: str

    def __init__(self, chart: Graph):
        self._chart = chart

    @staticmethod
    def _format_time_value(minutes: int) -> dict[str, str | int]:
        h = minutes // 60
        m = minutes % 60
        return {
            "label": f"{h}h {m}m" if h else f"{m}m",
            "value": minutes,
        }

    @abstractmethod
    def add_data(self, title: str, data: Iterable) -> None: ...

    @abstractmethod
    def add_labels(self, x_labels: Iterable, y_labels: Iterable) -> None: ...

    def add_title(self, title: str = "") -> None:
        self._chart.title = title or self.title

    def render(self) -> SVG:
        return self._chart.render_data_uri()


class TimePerCalendarChart(BaseChart):
    type = ChartType.LINE
    title = "Scheduled time per calendar"

    def add_data(self, title: str, data: Iterable[DailyStatistics]) -> None:
        self._chart.add(
            title=title,
            values=[self._format_time_value(s.minutes) for s in data],
        )

    def add_labels(self, x_labels: Iterable, y_labels: Iterable) -> None:
        self._chart.x_label_rotation = -45
        self._chart.x_labels = x_labels
        self._chart.y_labels = y_labels


class TimeTotalChart(BaseChart):
    type: ChartType = ChartType.STACKED_LINE
    title = "Scheduled time"

    def add_data(self, title: str, data: Iterable[DailyStatistics]) -> None:
        self._chart.add(
            title=title,
            values=[self._format_time_value(s.minutes) for s in data],
        )

    def add_labels(self, x_labels: Iterable, y_labels: Iterable) -> None:
        self._chart.x_label_rotation = -45
        self._chart.x_labels = x_labels
        self._chart.y_labels = y_labels


class PercentPerCalendarChart(BaseChart):
    type: ChartType = ChartType.PIE
    title = "Scheduled time relatively to other calendars"

    @staticmethod
    def _format_time_value_with_percent(minutes: int, percent: float) -> dict[str, str | int]:
        h = minutes // 60
        m = minutes % 60
        time = f"{h}h {m}m" if h else f"{m}m"
        return {
            "label": f"{percent}% ({time})",
            "value": minutes,
        }

    def add_data(self, title: str, data: Iterable[DailyStatistics]) -> None:
        minutes = sum(s.minutes for s in data)
        self._chart.add(
            title=title,
            values=self._format_time_value(minutes),
        )

    def add_labels(self, x_labels: Iterable, y_labels: Iterable) -> None:
        """
        There is no built-in option to add percents into labels.
        This will work only if `add_labels` is called after `add_data`.
        Otherwise labels will not contain percents, only hours and minutes.
        """
        total_minutes = sum(value["value"] for value, _ in self._chart.raw_series)
        for value, _ in self._chart.raw_series:
            minutes = value["value"]
            percent = round(minutes / total_minutes * 100, 1)
            value.update(self._format_time_value_with_percent(minutes, percent))
