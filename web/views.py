import logging
from datetime import datetime
from decimal import Decimal

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (FormView, TemplateView, RedirectView)
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
#from paypal.standard.forms import PayPalPaymentsForm

from web.api import (get_all_products, get_all_children, get_cart_total)
from web.forms import (DoctorForm, ChildForm,
                        UserForm, ParentProfileForm, LoginForm)
from web.models import (Product, OrderConfirmationId, Order, Child)


log = logging.getLogger(__name__)


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


class ProductView(LoginRequiredMixin, TemplateView):
    template_name = 'web/products.html'

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
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
        self.order_total = get_cart_total(request)
        # print("order total: %s" % self.order_total)
        # cfm_id_obj = OrderConfirmationId(total_price=self.order_total)
        # cfm_id_obj.save()
        # request.session["order_confirmation_no"] = cfm_id_obj.order_cfm
        # print("order cfm: %s" % cfm_id_obj.order_cfm)
        # for item in self.cart:
        #     order = Order(parent=request.user,
        #         child=Child.objects.get(id=item["child_id"]),
        #         product=Product.objects.get(id=item["id"]),
        #         quantity=item["quantity"],
        #         price=Decimal.from_float(item["price"]),
        #         for_date=datetime.strptime(item["for_date"], '%Y-%m-%d').date(),
        #         order_cfm=cfm_id_obj
        #     )
        #     order.save()
        #     print("item saved. id: %s" % order.pk)
        return super(PaymentView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        context["page_header"] = "Payment"
        context["order_total"] = self.order_total
        return context


# class PaymentView(LoginRequiredMixin, FormView):
#     form_class = PayPalPaymentsForm
#     template_name = 'web/payment.html'

#     def get_context_data(self, **kwargs):
#         context = super(PaymentView, self).get_context_data(**kwargs)
#         context["page_header"] = "Payment"
#         return context

#     def get_initial(self):
#         initial = super(PaymentView, self).get_initial()
#         initial.update({
#             "business": "receiver_email@example.com",
#             "amount": "0.99",
#             "item_name": "name of the item",
#             "invoice": "unique-invoice-id",
#             "notify_url": "https://www.example.com" + reverse('paypal-ipn'),
#             "return_url": "https://www.example.com/your-return-location/",
#             "cancel_return": "https://www.example.com/your-cancel-location/",
#         })
#         return initial