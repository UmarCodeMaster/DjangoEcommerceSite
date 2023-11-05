from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, TemplateView, CreateView, DetailView
from django.shortcuts import redirect, render
from ecom_app.models import Product, Company, Image, ProductReview, Shipping, CheckoutCart, CartItem
from ecom_app.forms import ShippingForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
import stripe
from datetime import datetime
from django.contrib import messages

stripe.api_key = "sk_test_51NayhRJ8QoauIX1Eh1K1YfigCE2of939McSk8M6eZdebf3kiLm40QosThnVsoHN7fhil7j4JFGA1hEfI2WTVB73W00GFEKA0DB"
# <-------------- LOG-IN -------------->


class Login(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

# <-------------- Register/signup-user -------------->


class Register(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().get(*args, **kwargs)

#---------------------------------------


class MyAccount(LoginRequiredMixin, TemplateView):
    template_name = 'my_account.html'





class CheckoutComplete(TemplateView):
    template_name = 'checkout_complete.html'


class Contectus(TemplateView):
    template_name = 'contact_us.html'


class AboutUS(TemplateView):
    template_name = 'about_us.html'


class FAQ(TemplateView):
    template_name = 'faq.html'


# <------------------ First-View-Of-Home-Page ------------------>


class HomeProductView(ListView):
    template_name = 'index.html'
    context_object_name = 'context'
    queryset = Product.objects.all()

    # <--------call to retrieves the context data from the parent class
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        mobile = self.request.GET.get('mobile')
        tablet = self.request.GET.get('tablet')

        if mobile is not None:
            context['mobile'] = Product.objects.filter(
                category=1, company=mobile)
        else:
            context['mobile'] = Product.objects.filter(category=1)

        if tablet is not None:
            context['tablet'] = Product.objects.filter(
                category=2, company=tablet)
        else:
            context['tablet'] = Product.objects.filter(category=2)

        context['trending'] = Product.objects.filter(trending=True)
        context['company'] = Company.objects.all()

        return context


# <-------------- Review-Api -------------->


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    
    def get_context_data(self, **kwargs):    # <--------call to retrieves the context data from the parent class
        context = super().get_context_data(**kwargs)
        context['image'] = Image.objects.filter(product_id=self.object.id)
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        product_id = self.kwargs.get('pk')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating and comment:
            ProductReview.objects.create(
                product_id=product_id,
                user=request.user,
                comment=comment,
                rating=rating
            )
        return redirect('product_detail', pk=product_id)


# <-------------- Search-Api -------------->


class SearchProductView(ListView):
    model = Product
    template_name = 'search_results.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('Search-area', '') or ''
        if search_input:
            context['product'] = context['product'].filter(
                name__startswith=search_input)
            context['search_input'] = search_input
        return context


#  <-------------- Product-Page -------------->


class ProductView(TemplateView):
    model = Product
    template_name = 'product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = Product.objects.all()
        return context


# <-------------- shipping-Method -------------->


class ProductShippingview(LoginRequiredMixin, CreateView):
    template_name = 'checkout_info.html'
    model = Shipping
    form_class = ShippingForm
    success_url = reverse_lazy('CheckoutPayment')


# <-------------- Add-To-Cart-Api -------------->


class Checkoutcart(LoginRequiredMixin, ListView):
    model = CheckoutCart
    template_name = 'checkout_cart.html'
    success_url = 'Checkoutinfo'

    def get_queryset(self):
        cart = CheckoutCart.objects.filter(user=self.request.user, is_completed=False)
        if not cart.count():
            CheckoutCart.objects.create(user=self.request.user, is_completed=False)
        return CheckoutCart.objects.filter(user=self.request.user, is_completed=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_show = context['object_list'].first().item.all()


        for item in product_show:                          #<---------- calculating the sub-total and total for a list of items based on their quantities and prices
            setattr(item, 'total', item.quantity * item.product.price)
        sub_total = sum(item.quantity * item.product.price for item in product_show)
        total = sub_total

        context['product_show'] = product_show
        context['sub_total'] = sub_total
        context['total'] = total
        return context

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('prod_id')
        operation = request.POST.get('operation')

        try:
            cart = CheckoutCart.objects.get(
                user=request.user, is_completed=False)
        except CheckoutCart.DoesNotExist:
            cart = CheckoutCart.objects.create(
                user=request.user, is_completed=False)
        
        cart_items = cart.item.filter(product_id=product_id)
        if cart_items.count():
            cart_item = cart_items.first()
            if operation == 'decrease':
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()
            elif operation == 'increase':
                cart_item.quantity += 1
                cart_item.save()
            elif operation == 'delete':
                cart_item.delete()
        else:
            cart_item = CartItem.objects.create(
                product_id=product_id,
                quantity=1
            )
            cart.item.add(cart_item)
        cart.save()
        cart_total = sum(item.product.price*item.quantity for item in cart.item.all())
        cart.total = cart_total
        cart.save()

        return redirect('checkout_cart')


# <-------------- Payment Method -------------->


class CheckOutPayment(LoginRequiredMixin, View):
    template_name = 'checkout_payment.html'

    def post(self, request, *args, **kwargs):
        payload = request.POST

        cardholder = payload.get('cardholder')
        cardnumber = payload.get('cardnumber')
        payment_type = str(payload.get('payment_type')).lower()

        mm = payload.get('mm')
        yy = payload.get('yy')
        number = payload.get('number')
        cardholder = payload.get('cardholder')

        required_values = ['cardholder', 'cardnumber', 'mm', 'yy', 'number']
        for value in required_values:
            if not payload.get(value):
                messages.error(request, f'{value} is required')
                return redirect('checkout_payment')

        cart = CheckoutCart.objects.filter(user=request.user, is_completed=False).first()

        dollars = sum(item.quantity * item.product.price for item in cart.item.all())
        price = dollars*100

        # https://stripe.com/docs/testing?testing-method=payment-methods#test-code
        stripe_tokens = {
            'paypal': 'pm_card_visa',  # using visa too for paypal method
            'visa': 'pm_card_visa',
            'master card': 'pm_card_mastercard',  
            'discover': 'pm_card_discover',
            }


        payment_intent = stripe.PaymentIntent.create(
            amount=int(price),
            currency="usd",
            payment_method_types=["card"],
            payment_method=stripe_tokens[payment_type],
            receipt_email=request.user.email or 'umar.ali@gmail.com'
        )
        confirm_payment = stripe.PaymentIntent.confirm(
            payment_intent.id,
            payment_method="pm_card_visa",
        )
        if confirm_payment.status == "succeeded":
            transaction_id = confirm_payment.id
            transaction_datetime = datetime.now()

        usercart = CheckoutCart.objects.filter(user=request.user, is_completed=False)
        cart = None
        if usercart.count():
            cart = usercart.first()
            cart.is_completed = True
            cart.save()

        shipping = 0
        sub_total = 0
        total = 0
        product_show = cart.item.all()
        for item in product_show:
            sub_total += item.quantity*item.product.price
        total += shipping+sub_total

        context = {
            "intent": confirm_payment,  
            "cart_image": cart,
            'product': cart,
            'product_show': product_show,
            'transaction_id': transaction_id,
            'transaction_datetime': transaction_datetime,
            "total": total,
        }
        return render(request, template_name="checkout_complete.html", context=context)

    def get(self, request):
        return render(request, self.template_name)
