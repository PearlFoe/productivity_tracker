from abc import ABC, abstractmethod
from collections.abc import Iterable

from pygal import Graph

from ..models.statistics import DailyStatistics

SVG = str


class BaseChart(ABC):
    def __init__(self, chart: Graph):
        self._chart = chart

    @abstractmethod
    def add_data(self, title: str, data: Iterable) -> None: ...

    @abstractmethod
    def add_labels(self, labels: Iterable[str]) -> None: ...

    def render(self) -> SVG:
        return self._chart.render()


class TimePerCalendarChart(BaseChart):
    def add_data(self, title: str, data: Iterable[DailyStatistics]) -> None:
        self._chart.add(
            title=title,
            values=(s.minutes for s in data),
        )

    def add_labels(self, labels: Iterable[str]) -> None:
        self._chart.x_label_rotation = -45
        self._chart.x_labels = labels


class TimeTotalChart(BaseChart):
    def add_data(self, title: str, data: Iterable[DailyStatistics]) -> None:
        self._chart.add(
            title=title,
            values=(s.minutes for s in data),
        )

    def add_labels(self, labels: Iterable[str]) -> None:
        self._chart.x_label_rotation = -45
        self._chart.x_labels = labels


class PercentPerCalendarChart(BaseChart):
    def add_data(self, title: str, data: Iterable[DailyStatistics]) -> None:
        self._chart.add(
            title=title,
            values=sum(s.minutes for s in data),
        )

    def add_labels(self, labels: Iterable[str] = ()) -> None:
        pass
