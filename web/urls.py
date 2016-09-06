from django.conf.urls import url

from web.views import (LoginView, LogoutView, HomeView, ContactView, 
    RegisterParentView, CartView, RegisterSuccessView, RegistrationView)


urlpatterns = [
    url(r'^(home)?$', HomeView.as_view(), name='home'),
    url(r'^contact$', ContactView.as_view(), name='contact'),
    url(r'^cart$', CartView.as_view(), name='cart'),

    ## site access url
    url(r'^register$', RegistrationView.as_view(), name='register'),
    url(r'^register/parent$', RegisterParentView.as_view(), name='register-parent'),
    url(r'^register/success$', RegisterSuccessView.as_view(), name='register-success'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),

    ## login required
    # url(r'^order$', OrderView.as_view(), name='order'),
    # url(r'^order-confirmation$', ContactView.as_view(), name='order-confirmation'),
    # url(r'^order-status$', OrderStatusView.as_view(), name='order_status'),
]