import calendar
import datetime

from django.utils.translation import ugettext_lazy as _

MONDAY = _('Monday')
TUESDAY = _('Tuesday')
WEDNESSDAY = _("Wednessday")
THURSDAY = _('Thursday')
FRIDAY = _('Friday')
EVERY_WEEK_DAY = _('Every Week Day')
EVERY_WEEK_DAY_NUM = 9

DAY_CHOICES = (
    (0, MONDAY),
    (1, TUESDAY),
    (2, WEDNESSDAY),
    (3, THURSDAY),
    (4, FRIDAY),
    (9, EVERY_WEEK_DAY)
)


def get_min_order_date_str():
    min_order_date = datetime.date.today() + datetime.timedelta(days=3)
    return min_order_date.strftime("%Y-%m-%d")


def get_max_order_date_str():
    today = datetime.date.today()
    if today.day >= 25:
        if today.month == 12:
            year = today.year + 1
            month = 1
        else:
            year = today.year
            month = today.month + 1
    else:
        year = today.year
        month = today.month
    last_day = calendar.monthrange(year, month)[1]
    d = datetime.datetime.strptime(''.join([str(year), '-', str(month), '-', str(last_day)]), "%Y-%m-%d")
    return d.strftime("%Y-%m-%d")
