from django.conf.urls import url

from web.views import (LoginView, LogoutView, HomeView, ContactView,
    RegisterParentView, RegisterSuccessView, RegistrationView,
    ProductView, OrderReviewView)
from web import api


urlpatterns = [
    url(r'^(home)?$', HomeView.as_view(), name='home'),
    url(r'^contact$', ContactView.as_view(), name='contact'),

    ## site access url
    url(r'^register$', RegistrationView.as_view(), name='register'),
    url(r'^register/parent$', RegisterParentView.as_view(), name='register-parent'),
    url(r'^register/success$', RegisterSuccessView.as_view(), name='register-success'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),

    ## login required
    url(r'^products$', ProductView.as_view(), name='products'),
    url(r'^order-review$', OrderReviewView.as_view(), name='order-review'),

    url(r'^api/get-cart$', api.get_cart, name='api-cart'),
    url(r'^api/add-to-cart/(?P<product_id>(\w+))/(?P<for_date>(\d{4}-\d{1,2}-\d{1,2}))$', api.add_to_cart, name='api-add-to-cart'),
    url(r'^api/remove-from-cart/(?P<product_id>(\w+))/(?P<for_date>[\d-]+)$', api.remove_from_cart, name='api-remove-from-cart'),
    url(r'^api/categories/(?P<category_id>\w+)$', api.get_categories, name='api-category'),
    url(r'^api/categories$', api.get_categories, name='api-categories'),
    url(r'^api/products/(?P<product_id>\w+)$', api.get_products, name='api-product'),
    url(r'^api/products$', api.get_products, name='api-products'),

    #url(r'^payment$', PaymentView.as_view(), name='payment')
]