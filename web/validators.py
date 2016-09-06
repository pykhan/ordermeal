from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _

@deconstructible
class TwoPasswordMatchValidator(validators.BaseValidator):
    message = _('Ensure this value is less than or equal to %(limit_value)s.')
    code = 'max_value'

    def compare(self, a, b):
        return a > b