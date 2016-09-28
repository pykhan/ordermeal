from django.conf.urls import url

from web.views import (LoginView, LogoutView, HomeView, ContactView,
    RegisterParentView, RegisterSuccessView, RegistrationView, ReportView,
    OrderView, OrderReviewView, RemoveFromCartView, PaymentView, ProfileView,
    PaymentConfirmationView)
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

    ## login required - class views
    url(r'^profile$', ProfileView.as_view(), name='profile'),
    url(r'^order$', OrderView.as_view(), name='order'),
    url(r'^order-review$', OrderReviewView.as_view(), name='order-review'),
    url(r'^remove-from-cart/(?P<child_id>(\d+))/(?P<product_id>(\d+))/(?P<for_date>(\d{4}-\d{1,2}-\d{1,2}))$',
        RemoveFromCartView.as_view(), name='remove-from-cart'),
    url(r'^payment$', PaymentView.as_view(), name='payment'),
    url(r'^report$', ReportView.as_view(), name='report'),
    url(r'^payment-confirmation$', PaymentConfirmationView.as_view(), name='payment-confirmation'),

    ## login required - api calls
    url(r'^confirm-payment/(?P<check_no>\w+)$', api.confirm_payment, name='confirm-payment'),
    url(r'^get-cart$', api.get_cart, name='api-cart'),
    url(r'^add-to-cart/(?P<child_id>(\d+))/(?P<product_id>(\d+))/(?P<for_date>(\d{4}-\d{1,2}-\d{1,2}))$', api.add_to_cart, name='api-add-to-cart'),
    url(r'^products/(?P<product_id>\d+)$', api.get_products, name='api-product'),
    url(r'^products$', api.get_products, name='api-products'),
    url(r'^products/(?P<for_date>(\d{4}-\d{1,2}-\d{1,2}))$', api.get_products, name='api-products'),
    url(r'^product-description/(?P<product_id>\d+)$', api.get_product_description, name='api-product-description'),
]