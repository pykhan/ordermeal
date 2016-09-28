from django.utils.translation import ugettext_lazy as _

MONDAY = _('Monday')
TUESDAY = _('Tuesday')
WEDNESSDAY = _("Wednessday")
THURSDAY = _('Thursday')
FRIDAY = _('Friday')
EVERY_WEEK_DAY = _('Every Week Day')

DAY_CHOICES = (
    (0, MONDAY),
    (1, TUESDAY),
    (2, WEDNESSDAY),
    (3, THURSDAY),
    (4, FRIDAY),
    (9, EVERY_WEEK_DAY)
)