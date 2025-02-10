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
    def _format_time_value(minutes: int) -> str:
        h = minutes // 60
        m = minutes % 60
        return f"{h}h {m}m" if h else f"{m}m"

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
        self._chart.add(title=title, values=[s.minutes for s in data], formatter=self._format_time_value)

    def add_labels(self, x_labels: Iterable, y_labels: Iterable) -> None:
        self._chart.x_label_rotation = -45
        self._chart.x_labels = x_labels
        self._chart.y_labels = y_labels


class TimeTotalChart(BaseChart):
    type: ChartType = ChartType.STACKED_LINE
    title = "Scheduled time"

    def add_data(self, title: str, data: Iterable[DailyStatistics]) -> None:
        self._chart.add(title=title, values=[s.minutes for s in data], formatter=self._format_time_value)

    def add_labels(self, x_labels: Iterable, y_labels: Iterable) -> None:
        self._chart.x_label_rotation = -45
        self._chart.x_labels = x_labels
        self._chart.y_labels = y_labels


class PercentPerCalendarChart(BaseChart):
    type: ChartType = ChartType.PIE
    title = "Scheduled time relatively to other calendars"

    def add_data(self, title: str, data: Iterable[DailyStatistics]) -> None:
        minutes = sum(s.minutes for s in data)
        self._chart.add(title=title, values=minutes, formatter=self._format_time_value)

    def add_labels(self, x_labels: Iterable, y_labels: Iterable) -> None:
        return
