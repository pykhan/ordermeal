from django.contrib import admin

from web.models import (Product, Child, ParentProfile,
                        OrderConfirmationId, Order)


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'parent_name', )
    empty_value_display = '-empty-'

    def parent_name(self, obj):
        return "%s %s" % (obj.parent.first_name, obj.parent.last_name)


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('parent_name', 'work_phone', 'cell_phone', )
    empty_value_display = '-empty-'

    def parent_name(self, obj):
        return "%s %s" % (obj.user.first_name, obj.user.last_name)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_price', 'description', 'expires_at', 'available_day', )
    ordering = ('expires_at', 'name')


@admin.register(OrderConfirmationId)
class OrderConfirmationIdAdmin(admin.ModelAdmin):
    list_display = ('order_cfm', 'other_order_cfm', 'total_price', 'has_paid', )
    ordering = ('has_paid', '-order_cfm', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('cfm_num', 'other_cfm', 'parent_name', 'child_name', 'product_name', 'quantity', 'price', 'for_date', 'has_paid', )
    ordering = ('-order_cfm', )

    def parent_name(self, obj):
        return "%s %s" % (obj.parent.first_name, obj.parent.last_name)

    def child_name(self, obj):
        return "%s" % obj.child.first_name

    def product_name(self, obj):
        return "%s" % obj.product.name

    def cfm_num(self, obj):
        return "%s" % obj.order_cfm.order_cfm

    def other_cfm(self, obj):
        return "%s" % obj.order_cfm.other_order_cfm

    def has_paid(self, obj):
        return obj.order_cfm.has_paid