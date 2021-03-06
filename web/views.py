import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import (HttpResponseRedirect)
from django.urls import (reverse_lazy)
from django.utils.decorators import method_decorator
from django.views.generic import (FormView, TemplateView, RedirectView, ListView)

from web import utils
from web.api import (get_all_children, get_cart_total, get_products_by_date)
from web.forms import (ChildForm, ChangePasswordForm, OrderDateForm,
                       UserForm, ParentProfileForm, LoginForm)
from web.models import (Order, ParentProfile)

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
    child_form = None
    parent_profile_form = None
    user_form = None
    is_successful = False

    def get(self, request, *args, **kwargs):
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
        return context

    def post(self, request, *args, **kwargs):
        self.child_form = ChildForm(request.POST, prefix='child_form')
        self.parent_profile_form = ParentProfileForm(request.POST, prefix='parent_profile_form')
        self.user_form = self.form_class(request.POST, prefix='user_form')

        if all([self.user_form.is_valid(),
                self.parent_profile_form.is_valid(),
                self.child_form.is_valid()]):
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

            return HttpResponseRedirect(redirect_to=reverse_lazy('ol:register-success'))
        else:
            if not self.user_form.is_valid():
                self.form_invalid(self.user_form)
            elif not self.parent_profile_form.is_valid():
                self.form_invalid(self.parent_profile_form)
            elif not self.child_form.is_valid():
                self.form_invalid(self.child_form)
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


class OrderView(LoginRequiredMixin, FormView):
    form_class = OrderDateForm
    template_name = 'web/order.html'
    success_url = reverse_lazy('ol:order')

    def form_valid(self, form):
        self.request.session["order_date"] = form["order_date"].data
        return super(OrderView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        order_date = self.request.session.get("order_date", None)
        context["page_header"] = "Available Items"
        context["date_form"] = context.pop("form")
        context["min_dt"] = utils.get_min_order_date_str()
        context["max_dt"] = utils.get_max_order_date_str()
        context["product_list"] = get_products_by_date(order_date) if order_date else None
        context["child_list"] = get_all_children(self.request.user)
        self.request.session["order_date"] = None
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
        pp = ParentProfile.objects.get(user=request.user)
        self.is_membership_paid = pp.is_membership_paid
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

    def get_context_data(self, **kwargs):
        context = super(PaymentConfirmationView, self).get_context_data(**kwargs)
        context["page_header"] = "Payment Confirmation"
        context["confirmation_number"] = self.request.session.get("confirmation_number")
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'web/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context["page_header"] = "My Profile"
        context["change_password_form"] = ChangePasswordForm(prefix='ch_pwd')
        return context

    def post(self, request, *args, **kwargs):
        change_password_form = ChangePasswordForm(request.POST, prefix='ch_pwd')
        if change_password_form.is_valid():
            user = User.objects.get(id=request.user.id)
            user.set_password(change_password_form["password"].data)
            user.save()
        else:
            raise Exception("Invalid password")
        return super(ProfileView, self).post(request, *args, **kwargs)


class ReportView(LoginRequiredMixin, ListView):
    template_name = 'web/report.html'
    model = Order
    queryset = None

    def get(self, request, *args, **kwargs):
        self.queryset = Order.objects.order_by('for_date')
        return super(ReportView, self).get(request, *args, **kwargs)
