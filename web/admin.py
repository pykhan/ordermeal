from django.contrib import admin

from web.models import (Category, Product, Doctor, Child, ParentProfile,
                        OrderConfirmationId, Order)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'work_phone', 'cell_phone',
        'address_1', 'address_2', 'city', 'state', 'zip_code', 'child', )
    empty_value_display = '-empty-'


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'birth_date', )
    empty_value_display = '-empty-'


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('address_1', 'address_2', 'city', 'state', 'zip_code', 'work_phone', 'cell_phone', )
    empty_value_display = '-empty-'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_price', 'description', 'category', 'expires_at')
    ordering = ('expires_at', 'category', 'name')


@admin.register(OrderConfirmationId)
class OrderConfirmationIdAdmin(admin.ModelAdmin):
    ordering = ('-order_cfm', )