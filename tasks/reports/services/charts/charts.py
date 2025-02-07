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

    def __init__(self, chart: Graph):
        self._chart = chart

    @abstractmethod
    def add_data(self, title: str, data: Iterable) -> None: ...

    @abstractmethod
    def add_labels(self, x_labels: Iterable, y_labels: Iterable) -> None: ...

    def render(self) -> SVG:
        return self._chart.render_data_uri()


class TimePerCalendarChart(BaseChart):
    type: ChartType = ChartType.LINE

    def add_data(self, title: str, data: Iterable[DailyStatistics]) -> None:
        self._chart.add(
            title=title,
            values=[s.minutes for s in data],
        )

    def add_labels(self, x_labels: Iterable, y_labels: Iterable) -> None:
        self._chart.x_label_rotation = -45
        self._chart.x_labels = x_labels
        self._chart.y_labels = y_labels


class TimeTotalChart(BaseChart):
    type: ChartType = ChartType.STACKED_LINE

    def add_data(self, title: str, data: Iterable[DailyStatistics]) -> None:
        self._chart.add(
            title=title,
            values=[s.minutes for s in data],
        )

    def add_labels(self, x_labels: Iterable, y_labels: Iterable) -> None:
        self._chart.x_label_rotation = -45
        self._chart.x_labels = x_labels
        self._chart.y_labels = y_labels


class PercentPerCalendarChart(BaseChart):
    type: ChartType = ChartType.PIE

    def add_data(self, title: str, data: Iterable[DailyStatistics]) -> None:
        self._chart.add(
            title=title,
            values=sum(s.minutes for s in data),
        )

    def add_labels(self, x_labels: Iterable, y_labels: Iterable) -> None:
        pass
