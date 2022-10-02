from datetime import timedelta

from django.db.models import QuerySet

from ..models import FunctionType, LogEntry
from .utils import (
    PPL_END_DATE,
    PPL_START_DATE,
    AuthenticatedTemplateView,
    ExperienceRecord,
    TotalsRecord,
    compute_totals,
)


class ExperienceIndexView(AuthenticatedTemplateView):
    template_name = "logbook/experience_list.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {
            "ppl": get_ppl_experience(
                LogEntry.objects.filter(
                    departure_time__gte=PPL_START_DATE,
                    departure_time__lt=PPL_END_DATE,
                ),
            ),
            "night": get_night_experience(LogEntry.objects.filter(night=True)),
            "ir": get_ir_experience(LogEntry.objects.filter(departure_time__gte=PPL_START_DATE)),
            "cpl": get_cpl_experience(LogEntry.objects.filter(departure_time__gte=PPL_START_DATE)),
        }


def get_ppl_experience(log_entries: QuerySet) -> dict:
    return {
        "Dual instruction": ExperienceRecord(
            required=TotalsRecord(time=timedelta(hours=25), landings=0),
            accrued=compute_totals(log_entries.filter(time_function=FunctionType.DUAL.name)),
        ),
        "Supervised solo": ExperienceRecord(
            required=TotalsRecord(time=timedelta(hours=10), landings=0),
            accrued=compute_totals(log_entries.filter(time_function=FunctionType.PIC.name)),
        ),
        "Cross-country solo": ExperienceRecord(
            required=TotalsRecord(time=timedelta(hours=5), landings=0),
            accrued=compute_totals(log_entries.filter(time_function=FunctionType.PIC.name, cross_country=True)),
        ),
        "Total hours": ExperienceRecord(
            required=TotalsRecord(time=timedelta(hours=45), landings=0),
            accrued=compute_totals(log_entries),
        ),
    }


def get_night_experience(log_entries: QuerySet) -> dict:
    return {
        "Solo full-stop landings": ExperienceRecord(
            required=TotalsRecord(time=timedelta(hours=0), landings=5),
            accrued=compute_totals(log_entries.filter(time_function=FunctionType.PIC.name), full_stop=True),
        ),
        "Dual instruction": ExperienceRecord(
            required=TotalsRecord(time=timedelta(hours=3), landings=0),
            accrued=compute_totals(log_entries.filter(time_function=FunctionType.DUAL.name)),
        ),
        "Dual cross-country (>27 NM)": ExperienceRecord(
            required=TotalsRecord(time=timedelta(hours=1), landings=0),
            accrued=compute_totals(log_entries.filter(time_function=FunctionType.DUAL.name, cross_country=True)),
        ),
        "Total hours": ExperienceRecord(
            required=TotalsRecord(time=timedelta(hours=5), landings=0),
            accrued=compute_totals(log_entries),
        ),
    }


def get_ir_experience(log_entries: QuerySet) -> dict:
    return {
        "Cross-country PIC": ExperienceRecord(
            required=TotalsRecord(time=timedelta(hours=50), landings=0),
            accrued=compute_totals(log_entries.filter(time_function=FunctionType.PIC.name, cross_country=True)),
        ),
    }


def get_cpl_experience(log_entries: QuerySet) -> dict:
    return {
        "PIC": ExperienceRecord(
            required=TotalsRecord(time=timedelta(hours=100), landings=0),
            accrued=compute_totals(log_entries.filter(time_function=FunctionType.PIC.name)),
        ),
        "Cross-country PIC": ExperienceRecord(
            required=TotalsRecord(time=timedelta(hours=20), landings=0),
            accrued=compute_totals(log_entries.filter(time_function=FunctionType.PIC.name, cross_country=True)),
        ),
        "Total hours": ExperienceRecord(
            required=TotalsRecord(time=timedelta(hours=200), landings=0),
            accrued=compute_totals(log_entries),
        ),
    }
