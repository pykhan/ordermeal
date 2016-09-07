from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from localflavor.us.models import PhoneNumberField
from localflavor.us.us_states import STATE_CHOICES
    

class ModelSaveMixin(object):
    created_at = models.DateField(verbose_name=_('Created At'), editable=False)
    updated_at = models.DateField(verbose_name=_('Updated At'))

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(ModelSaveMixin, self).save(*args, **kwargs)


class ParentProfile(ModelSaveMixin, models.Model):
    user = models.OneToOneField(User, verbose_name=_("Parent's Name"))
    cell_phone = PhoneNumberField(verbose_name=_('Cell Phone'))
    home_phone = PhoneNumberField(verbose_name=_('Home Phone'), blank=True, null=True)
    work_phone = PhoneNumberField(verbose_name=_('Work Phone'), blank=True, null=True)
    address_1 = models.CharField(verbose_name=_('Address 1'), max_length=100)
    address_2 = models.CharField(verbose_name=_('Address 2'), max_length=100, blank=True, null=True)
    city = models.CharField(verbose_name=_('City'), max_length=100)
    state = models.CharField(max_length=2, default=_('NJ'), choices=STATE_CHOICES)
    zip_code = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return "%s, %s" % (self.user.last_name, self.user.first_name)

    class Meta:
        verbose_name = _("Parent Profile")
        verbose_name_plural = _("Parent Profiles")


class Child(ModelSaveMixin, models.Model):
    parent = models.ForeignKey(User, verbose_name=_('Parent'), blank=True, null=True)
    first_name = models.CharField(verbose_name=_('First Name'), max_length=30)
    middle_name = models.CharField(verbose_name=_('Middle Name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(verbose_name=_('Last Name'), max_length=30)
    birth_date = models.DateField(verbose_name=_('Birth Date'), blank=True, null=True)
    allergies = models.TextField(verbose_name=_('Allergies'), blank=True, null=True)

    def __str__(self):
        return "%s, %s" % (self.last_name, self.first_name)

    class Meta:
        verbose_name = _("Child")
        verbose_name_plural = _("Children")


class Doctor(ModelSaveMixin, models.Model):
    child = models.ForeignKey(Child, verbose_name=_("Child"))
    first_name = models.CharField(verbose_name=_('First Name'), max_length=30, blank=True, null=True)
    middle_name = models.CharField(verbose_name=_('Middle Name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(verbose_name=_('Last Name'), max_length=30, blank=True, null=True)
    work_phone = PhoneNumberField(verbose_name=_('Work Phone'), blank=True, null=True)
    cell_phone = PhoneNumberField(verbose_name=_('Cell Phone'), blank=True, null=True)
    address_1 = models.CharField(verbose_name=_('Address 1'), max_length=100, blank=True, null=True)
    address_2 = models.CharField(verbose_name=_('Address 2'), max_length=100, blank=True, null=True)
    city = models.CharField(verbose_name=_('City'), max_length=100, blank=True, null=True)
    state = models.CharField(max_length=2, default=_('NJ'), blank=True, null=True, choices=STATE_CHOICES)
    zip_code = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return "%s, %s" % (self.last_name, self.first_name)

    class Meta:
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")


class Category(ModelSaveMixin, models.Model):
    name = models.CharField(max_length=50, verbose_name="Category Name")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Product(ModelSaveMixin, models.Model):
    name = models.CharField(max_length=50)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
    category = models.ForeignKey(Category)
    expires_at = models.DateField(verbose_name=_('Expires At'), blank=True, null=True)

    def __str__(self):
        return '%s (@ %s)' % (self.name, self.unit_price)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
