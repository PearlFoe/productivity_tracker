from collections.abc import Iterable
from datetime import date
from math import ceil

from jinja2 import Template

from ..constants import REPORT_DATE_FORMAT
from ..models.statistics import DailyStatistics, StatisticsExtremum
from .charts.chart_sets import BaseChartSet
from .charts.charts import ChartType


class UserReportBuilder:
    def __init__(self, chart_set: BaseChartSet):
        self._chart_set = chart_set

    def _get_template_file(self, file: str) -> str:
        with open(file) as f:
            return f.read()

    def _get_rendered_charts(self) -> dict:
        return {chart_name: chart.render() for chart_name, chart in self._chart_set.charts.items()}

    @staticmethod
    def __get_hour_labels(max_hour: int) -> list[dict]:
        return [{"label": f"{h}h" if h else "", "value": h * 60} for h in range(max_hour + 1)]

    def _get_hours_labels(self, chart_type: ChartType, extremums: StatisticsExtremum) -> list[dict]:
        match chart_type:
            case ChartType.LINE:
                max_hour = ceil(extremums.one_calendar_minutes_sum / 60)
                return self.__get_hour_labels(max_hour)
            case ChartType.STACKED_LINE:
                max_hour = ceil(extremums.all_calendars_minutes_sum / 60)
                return self.__get_hour_labels(max_hour)
            case _:
                return []

    @staticmethod
    def _get_dates_labels(dates: Iterable[date]) -> list[str]:
        return [d.strftime(REPORT_DATE_FORMAT) for d in dates]

    def add_calendar_statistics(self, calendar_name: str, statistics: Iterable[DailyStatistics]) -> None:
        for chart in self._chart_set.charts.values():
            chart.add_data(calendar_name, statistics)

    def add_labels(self, extremums: StatisticsExtremum, dates: Iterable[date]) -> None:
        for chart in self._chart_set.charts.values():
            chart.add_labels(
                y_labels=self._get_hours_labels(chart.type, extremums), x_labels=self._get_dates_labels(dates)
            )

    def build_html(self) -> str:
        html = self._get_template_file(self._chart_set.template)
        template = Template(html)
        rendered_charts = self._get_rendered_charts()
        return template.render(rendered_charts)
