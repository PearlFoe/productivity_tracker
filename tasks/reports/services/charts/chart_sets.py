from pydantic import BaseModel, ConfigDict
from pygal import Line, Pie, StackedLine

from .charts import BaseChart, PercentPerCalendarChart, TimePerCalendarChart, TimeTotalChart
from .styles import DEFAULT_STYLE


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
        "time_per_calendar": TimePerCalendarChart(chart=Line(style=DEFAULT_STYLE)),
        "time_total": TimeTotalChart(chart=StackedLine(style=DEFAULT_STYLE, fill=True)),
        "percent_per_calendar": PercentPerCalendarChart(chart=Pie(style=DEFAULT_STYLE)),
    }
