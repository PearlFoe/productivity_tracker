from collections.abc import Iterable
from datetime import date

from jinja2 import Template

from ..constants import REPORT_DATE_FORMAT
from ..models.statistics import DailyStatistics
from .charts.chart_sets import BaseChartSet


class UserReportBuilder:
    def __init__(self, chart_set: BaseChartSet):
        self._chart_set = chart_set

    def _get_template_file(self, file: str) -> str:
        with open(file) as f:
            return f.read()

    def _get_rendered_charts(self) -> dict:
        return {chart_name: chart.render() for chart_name, chart in self._chart_set.charts.items()}

    def add_calendar_statistics(self, calendar_name: str, statistics: Iterable[DailyStatistics]) -> None:
        for chart in self._chart_set.charts.values():
            chart.add_data(calendar_name, statistics)

    def add_labels(self, dates: Iterable[date]) -> None:
        formated_dates = [d.strftime(REPORT_DATE_FORMAT) for d in dates]
        for chart in self._chart_set.charts.values():
            chart.add_labels(labels=formated_dates)

    def build_html(self) -> str:
        html = self._get_template_file(self._chart_set.template)
        template = Template(html)
        rendered_charts = self._get_rendered_charts()
        return template.render(rendered_charts)
