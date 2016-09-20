import logging
from datetime import datetime
from decimal import Decimal

#import paypalrestsdk
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (FormView, TemplateView, RedirectView)
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm

from web.api import (get_all_products, get_all_children, get_cart_total)
from web.forms import (DoctorForm, ChildForm,
                        UserForm, ParentProfileForm, LoginForm)
from web.models import (Product, OrderConfirmationId, Order, Child, ParentProfile)


log = logging.getLogger(__name__)
# paypalrestsdk.configure({
#   "mode": "sandbox", # sandbox or live
#   "client_id": "AeUbUlYRgl5DJPvotj1UmGIswdlQpyXm3qPJq3ZBQTUOCQtkEsCpCytFYtdDvNu_LnFKWU-fRUDHylz4",
#   "client_secret": "EIA7iByWPUprfEtesDHMdh8SaCZ_kdKMfej3qEbr5R5cJ65j-kKj9Qc07divU1AiaE8CXZINV7EAvaZ7" })


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class HomeView(TemplateView):
    template_name = 'web/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["page_header"] = "Home"
        return context


class ContactView(TemplateView):
    template_name = 'web/contact.html'

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context["page_header"] = "Contact"
        return context


class RegistrationView(RedirectView):
    url = reverse_lazy('ol:register-parent')


class RegisterParentView(FormView):
    template_name = 'web/register-parent.html'
    success_url = reverse_lazy('ol:register-success')
    form_class = UserForm
    doctor_form = None
    child_form = None
    parent_profile_form = None
    user_form = None
    is_successful = False

    def get(self, request, *args, **kwargs):
        self.doctor_form = DoctorForm(prefix='doctor_form')
        self.child_form = ChildForm(prefix='child_form')
        self.parent_profile_form = ParentProfileForm(prefix='parent_profile_form')
        self.user_form = self.form_class(prefix='user_form')
        return super(RegisterParentView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RegisterParentView, self).get_context_data(**kwargs)
        context["page_header"] = "Parent Registration"
        context["user_form"] = self.user_form
        context["parent_profile_form"] = self.parent_profile_form
        context["child_form"] = self.child_form
        context["doctor_form"] = self.doctor_form
        return context

    def post(self, request, *args, **kwargs):
        self.doctor_form = DoctorForm(request.POST, prefix='doctor_form')
        self.child_form = ChildForm(request.POST, prefix='child_form')
        self.parent_profile_form = ParentProfileForm(request.POST, prefix='parent_profile_form')
        self.user_form = self.form_class(request.POST, prefix='user_form')

        if all([self.user_form.is_valid(),
                self.parent_profile_form.is_valid(),
                self.child_form.is_valid(),
                self.doctor_form.is_valid()]):
            ## save user
            parent = self.user_form.save(commit=False)
            parent.set_password(self.user_form["password"].data)
            parent.is_active = True
            parent.save()

            ## save parent profile
            parent_profile = self.parent_profile_form.save(commit=False)
            parent_profile.user_id = parent.id
            parent_profile.save()

            if self.child_form.has_changed():
                ## save child info
                child = self.child_form.save(commit=False)
                child.parent_id = parent.id
                child.save()

                if self.doctor_form.has_changed():
                    ## save doctor info
                    doctor = self.doctor_form.save(commit=False)
                    doctor.child_id = child_id
                    doctor.save()

            return HttpResponseRedirect('/web/register/success')
        else:
            print("invalid form")
        return super(RegisterParentView, self).post(request, *args, **kwargs)

    def form_invalid(self, form):
        print("invalid registration: %s" % form.errors)
        return super(RegisterParentView, self).form_invalid(form)


class RegisterSuccessView(TemplateView):
    template_name = 'web/register-success.html'

    def get_context_data(self, **kwargs):
        context = super(RegisterSuccessView, self).get_context_data(**kwargs)
        context["page_header"] = "Registration Successful"
        return context


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'web/login.html'
    success_url = reverse_lazy('ol:home')
    next_url = None

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context["page_header"] = "Please sign in"
        return context

    def get(self, request, *args, **kwargs):
        self.next_url = request.GET.get("next")
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        username = form["username"].data
        password = form["password"].data
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                profile = ParentProfile.objects.get(user=user)
                self.request.session["is_membership_paid"] = profile.is_membership_paid
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        print("invalid form: %s" % form.errors)
        return super(LoginView, self).form_invalid(form)

    def get_success_url(self):
        response = super(LoginView, self).get_success_url()
        if self.next_url:
            response = HttpResponseRedirect(redirect_to=self.next_url)
        return response


class LogoutView(RedirectView):
    url = reverse_lazy('ol:home')

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).dispatch(request, *args, **kwargs)


##################################################################################################


class OrderView(LoginRequiredMixin, TemplateView):
    template_name = 'web/order.html'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context["page_header"] = "Available Items"
        context["product_list"] = get_all_products()
        context["child_list"] = get_all_children(self.request.user)
        return context


class OrderReviewView(LoginRequiredMixin, TemplateView):
    template_name = 'web/order-review.html'
    cart_total = 0.00

    def get_context_data(self, **kwargs):
        context = super(OrderReviewView, self).get_context_data(**kwargs)
        context["page_header"] = "Order Review"
        context["cart"] = self.request.session.get("cart", None)
        context["min_date"] = None
        context["cart_total"] = self.cart_total
        return context

    def get(self, request, *args, **kwargs):
        self.cart_total = get_cart_total(request)
        return super(OrderReviewView, self).get(request, *args, **kwargs)


class RemoveFromCartView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('ol:order-review')

    def dispatch(self, request, *args, **kwargs):
        cart = request.session.get("cart", [])
        if cart:
            product_id = kwargs.get("product_id")
            for_date = kwargs.get("for_date")
            for item in cart:
                if item["id"] == int(product_id) and item["for_date"] == for_date:
                    cart.remove(item)
                    break
            request.session["cart"] = cart
        return super(RemoveFromCartView, self).dispatch(request, *args, **kwargs)


class PaymentView(LoginRequiredMixin, TemplateView):
    template_name = 'web/payment.html'

    def get(self, request, *args, **kwargs):
        self.cart = request.session.get("cart", [])
        self.is_membership_paid = request.session.get("is_membership_paid", False)
        self.order_total = get_cart_total(request)
        self.order_total_with_membership_fee = self.order_total if self.is_membership_paid else self.order_total + 1
        request.session["order_total"] = self.order_total
        request.session["order_total_with_membership_fee"] = self.order_total_with_membership_fee
        return super(PaymentView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        context["page_header"] = "Payment"
        context["order_total"] = self.order_total
        context["order_total_with_membership_fee"] = self.order_total_with_membership_fee
        context["is_membership_paid"] = self.is_membership_paid
        return context


class PaymentConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = 'web/payment-confirmation.html'
    confirmation_number = None
    paypal_confirmation = None

    # def get(self, request, *args, **kwargs):
    #     self.confirmation_number = request.session.get("order_confirmation_no", None)
    #     cart_total = get_cart_total(request)
    #     paypal_charge = cart_total * 0.05
    #     total_charge = cart_total + paypal_charge
    #     item_list = []
    #     for item in request.sessioin.get("cart"):
    #         item_list.append({
    #             "name": item["name"],
    #             "sku": item["id"],
    #             "price": str(item["price"]),
    #             "quantity": item["quantity"]
    #         },)
    #     payment = paypalrestsdk.Payment({
    #         "intent": "sale",
    #         "payer": {
    #             "payment_method": "paypal"
    #         },
    #         "redirect_urls": {
    #             "return_url": "http://localhost:8000/payment/execute",
    #             "cancel_url": "http://localhost:8000/"
    #         },
    #         "transactions": [{

    #             # ItemList
    #             "item_list": {
    #                 "items": item_list
    #             },

    #             # Amount
    #             # Let's you specify a payment amount.
    #             "amount": {
    #                 "total": str(total_charge),
    #                 "currency": "USD"},
    #             "description": "This is the payment transaction description."
    #         }]
    #     })
    #     if payment.create():
    #         self.paypal_confirmation = payment.id
    #         print("Payment[%s] created successfully" % (payment.id))
    #         # Redirect the user to given approval url
    #         for link in payment.links:
    #             if link.method == "REDIRECT":
    #                 # Convert to str to avoid google appengine unicode issue
    #                 # https://github.com/paypal/rest-api-sdk-python/pull/58
    #                 redirect_url = str(link.href)
    #                 print("Redirect for approval: %s" % (redirect_url))
    #     else:
    #         print("Error while creating payment:")
    #         print(payment.error)
    #     return super(PaymentConfirmationView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PaymentConfirmationView, self).get_context_data(**kwargs)
        context["page_header"] = "Payment Confirmation"
        context["confirmation_number"] = self.confirmation_number
        return context