from datetime import date

from django.contrib import sessions
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse

from web.models import (Category, Product)


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
    'S-101': {
        'code': 'S-101',
        'message': 'Cart has been updated successfully.'
    }, 
    'S-102': {
        'code': 'S-102',
        'message': 'Item has been removed successfully.'
    },
}


def get_all_products(product_id=None):
    if product_id:
        products = Product.objects.filter(id=product_id, is_active=True, expires_at__gte=date.today())
    else:
        products = Product.objects.filter(is_active=True, expires_at__gte=date.today())
    products_json = []
    for product in products:
        products_json.append({
            product.id: {
                    'name': product.name,
                    'unit_price': product.unit_price,
                    'description': product.description,
                    'category_id': product.category.id
                }
        })
    return products_json


@login_required
def get_products(request, product_id=None):
    api_resp = {
        'status': 'success',
        'payloads': get_all_products(product_id=product_id)
    }
    return JsonResponse(api_resp)


@login_required
def get_categories(request, category_id=None):
    api_resp = {}
    if category_id:
        categories = Category.objects.filter(id=category_id)
        if categories:
            category = categories[0]
            api_resp.update(status='success',
                payloads=[{
                    category.id: {
                        'name': product.name
                    }
                }])
        else:
            api_resp.update(status='failure', payloads=[API_CODES.get('E-102')])
    else:
        categories = Category.objects.all()
        payloads = []
        for category in categories:
            payloads.append({
                category.id: {
                    'name': category.name
                }
            })
        api_resp.update(status='success', payloads=payloads)
    return JsonResponse(data)


@login_required
def update_cart(request, product_id, quantity):
    api_resp = {}
    cart = request.session.get("cart", {})

    try:
        product = Product.objects.get(id=product_id)
    except Exception as e:
        api_resp.update(status='failure', payloads=[API_CODES.get('E-103')])
        print("Error: update_cart: %s" % e)
    else:
        if product_id not in cart:    
            cart[product_id] = {
                'name': product.name,
                'quantity': str(quantity),
                'total': str(product.unit_price * int(quantity))
            }
            request.session["cart"] = cart
        else:
            item = cart.get(product_id)
            if int(quantity) > 0:
                item.update(name=product.name, quantity=str(quantity), total=str(product.unit_price * int(quantity)))
                cart[product_id] = item
                request.session["cart"] = cart
            else:
                cart.pop(product_id)
        api_resp.update(status='success', payloads=[API_CODES.get('S-101')])
    return JsonResponse(api_resp)


@login_required
def remove_from_cart(request, product_id):
    api_resp = {}
    cart = request.session.get("cart", None)
    print(cart)

    if not cart:
        api_resp.update(status='failure', payloads=[API_CODES.get('E-104')])

    if product_id in cart:
        cart.pop(product_id)
        request.session["cart"] = cart
        api_resp.update(status='success', payloads=[API_CODES.get('S-102')])
    else:
        api_resp.update(status='failure', payloads=[API_CODES.get('E-105')])
    
    return JsonResponse(api_resp)


@login_required
def get_cart(request):
    api_resp = {}
    cart = request.session.get("cart", None)
    api_resp.update(status='success', payloads=[cart])
    return JsonResponse(api_resp)


def get_cart_total(request):
    ## calculate cart total and return it from here.
    pass