import logging
from datetime import date
from datetime import datetime
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse

from web.models import (Product, Child, OrderConfirmationId, Order)

EVERY_WEEK_DAY = 9

log = logging.getLogger(__name__)

API_CODES = {
    'E-101': {
        'code': 'E-101',
        'message': 'Product not found.'
    },
    'E-102': {
        'code': 'E-102',
        'message': 'Category not found.'
    },
    'E-103': {
        'code': 'E-103',
        'message': 'Product matching query does not exist.'
    },
    'E-104': {
        'code': 'E-104',
        'message': 'Cart is empty.'
    },
    'E-105': {
        'code': 'E-105',
        'message': 'Item dos not exist in cart. Nothing to remove.'
    },
    'E-106': {
        'code': 'E-106',
        'message': 'Your session may have expired. Please login again and order.'
    },
    'S-101': {
        'code': 'S-101',
        'message': 'Item added in cart.'
    },
    'S-102': {
        'code': 'S-102',
        'message': 'Item has been removed successfully.'
    },
    'S-103': {
        'code': 'S-103',
        'message': 'Your order has been placed successfully.'
    },
}


def get_all_products(product_id=None):
    if product_id:
        products = Product.objects.filter(id=product_id, expires_at__gte=date.today()).exclude(is_active=False)
    else:
        products = Product.objects.filter(is_active=True, expires_at__gte=date.today())
    products_json = []
    for product in products:
        products_json.append({
            'id': product.id,
            'name': product.name,
            'unit_price': product.unit_price,
            'description': product.description
        }, )
    return products_json


def get_all_children(parent):
    child_list = []
    children = Child.objects.filter(parent=parent)
    if children:
        for child in children:
            child_list.append({
                'id': child.id,
                'first_name': child.first_name,
                'last_name': child.last_name
            }, )
    return child_list


def get_cart_total(request):
    cart_total = 0.00
    cart = request.session.get("cart", None)
    if cart:
        for item in cart:
            cart_total = cart_total + item["price"]
    return cart_total


def session_cleanup(request):
    request.session.pop("cart")
    request.session.pop("order_total_with_membership_fee")
    request.session.pop("order_total")


def get_products_by_date(for_date):
    wd = datetime.strptime(for_date, "%Y-%m-%d").date().weekday()
    products = Product.objects.filter(Q(available_day=wd) |
                                      Q(available_day=EVERY_WEEK_DAY)).exclude(is_active=False,
                                                                               expires_at__lt=date.today())
    products_json = []
    for product in products:
        products_json.append({
            'id': product.id,
            'name': product.name,
            'unit_price': product.unit_price
        }, )
    return products_json


@login_required
def get_products(request, for_date):
    return JsonResponse({
        'status': 'success',
        'payloads': get_products_by_date(for_date=for_date)
    })


@login_required
def add_to_cart(request, child_id, product_id, for_date):
    api_resp = {}
    cart = request.session.pop("cart", [])

    try:
        product = Product.objects.get(id=product_id)
        child = Child.objects.get(id=child_id)
    except Exception as e:
        api_resp.update(status='failure', payloads=[API_CODES.get('E-103')])
        log.error("Error: update_cart: %s" % e)
    else:
        is_match = False
        if len(cart) > 0:
            for item in cart:
                if child.id == item["child_id"] and product.id == item["id"] and for_date == item["for_date"]:
                    item["quantity"] = item["quantity"] + 1
                    item["price"] = item["price"] + float(product.unit_price)
                    is_match = True

            if not is_match:
                cart.append({
                    'id': product.id,
                    'child_id': child.id,
                    'child_name': child.first_name,
                    'name': product.name,
                    'quantity': 1,
                    'price': float(product.unit_price),
                    'for_date': for_date
                }, )
        else:
            cart.append({
                'id': product.id,
                'child_id': child.id,
                'child_name': child.first_name,
                'name': product.name,
                'quantity': 1,
                'price': float(product.unit_price),
                'for_date': for_date
            }, )
        request.session["cart"] = cart
        api_resp.update(status='success', payloads=[API_CODES.get('S-101')])
    return JsonResponse(api_resp)


@login_required
def remove_from_cart(request, product_id, for_date):
    api_resp = {}
    cart = request.session.get("cart", [])

    if cart:
        cart = [item for item in cart if item["id"] != int(product_id) and item["for_date"] != for_date]
        request.session["cart"] = cart
        api_resp.update(status='success', payloads=[API_CODES.get('S-102')])
    else:
        api_resp.update(status='failure', payloads=[API_CODES.get('E-104')])
    return JsonResponse(api_resp)


@login_required
def get_cart(request):
    api_resp = {}
    cart = request.session.get("cart", [])
    api_resp.update(status='success', payloads=cart)
    return JsonResponse(api_resp)


@login_required
def confirm_payment(request, check_no):
    api_resp = {}
    total_charge = request.session.get("order_total_with_membership_fee", None)
    cart = request.session.get("cart", None)
    if all([total_charge, cart]):
        other_order_cfm = (request.user.last_name + "-Check-" + check_no).title()
        last_order_obj = OrderConfirmationId.objects.order_by('-order_cfm')
        if last_order_obj:
            last_order = last_order_obj[0].order_cfm + 1
        else:
            last_order = 1001
        cfm_id_obj = OrderConfirmationId(order_cfm=last_order, other_order_cfm=other_order_cfm,
                                         total_price=Decimal.from_float(total_charge))
        cfm_id_obj.save()
        for item in cart:
            Order(parent=request.user,
                  child=Child.objects.get(id=item["child_id"]),
                  product=Product.objects.get(id=item["id"]),
                  quantity=item["quantity"],
                  price=Decimal.from_float(item["price"]),
                  for_date=datetime.strptime(item["for_date"], '%Y-%m-%d').date(),
                  order_cfm=cfm_id_obj
                  ).save()
        api_resp.update(status='success', payloads=[API_CODES.get("S-103"), {'confirmation_no': cfm_id_obj.order_cfm}])
        session_cleanup(request)
    else:
        api_resp.update(status='error', payloads=[API_CODES.get("E-106")])
    return JsonResponse(api_resp)


@login_required
def get_product_description(request, product_id):
    api_resp = {}
    product_obj = Product.objects.get(id=product_id)
    api_resp.update(status='success', payloads=[{'message': product_obj.description}])
    return JsonResponse(api_resp)
