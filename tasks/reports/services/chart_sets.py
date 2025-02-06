from pydantic import BaseModel, ConfigDict
from pygal import Line, Pie, StackedLine

from .charts import BaseChart, PercentPerCalendarChart, TimePerCalendarChart, TimeTotalChart


class BaseChartSet(BaseModel):
    template: str
    charts: dict[str, BaseChart]

    model_config = ConfigDict(
        frozen=True,
        arbitrary_types_allowed=True,
    )


class UserReportChartSet(BaseChartSet):
    template: str = "tasks/reports/templates/user_report.html"
    charts: dict[str, BaseChart] = {
        "time_per_calendar": TimePerCalendarChart(chart=Line()),
        "time_total": TimeTotalChart(chart=StackedLine()),
        "percent_per_calendar": PercentPerCalendarChart(chart=Pie()),
    }
