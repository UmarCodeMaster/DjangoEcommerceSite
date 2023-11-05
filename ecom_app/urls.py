from django.urls import path
from .views import HomeProductView,Login,Register,ProductDetailView,SearchProductView,Checkoutcart,CheckoutComplete,Contectus,CheckOutPayment,MyAccount,AboutUS,FAQ,ProductView,ProductShippingview,Mobiles,Tablets
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/',Login.as_view(),name='login'),

    path('Logout/',LogoutView.as_view(next_page='home'), name='Logout'),

    path('Register/',Register.as_view(),name='Register'),

    path('',HomeProductView.as_view(),name='home'),

    path('ProductView/',ProductView.as_view(),name='ProductView'),

    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    
    path('SearchResult/',SearchProductView.as_view(),name='SearchResult'),

    path("checkout_cart/",Checkoutcart.as_view(), name="checkout_cart"),

    path('CheckoutComplete/',CheckoutComplete.as_view(),name='Checkoutcomplete'),

    path('ContectUs/',Contectus.as_view(),name='Contectus'),

    path('CheckoutPayment/',CheckOutPayment.as_view(),name='CheckoutPayment'),

    path('Checkoutinfo/',ProductShippingview.as_view(),name='Checkoutinfo'),

    path('MyAccount/',MyAccount.as_view(),name='MyAccount'),

    path('AboutUS/',AboutUS.as_view(),name='AboutUS'),

    path('faq/',FAQ.as_view(),name='FAQ'),
    
    path("list_mobile/",Mobiles.as_view(), name="list_mobile"),
    path("list_tablet/",Tablets.as_view(), name="list_tablet"),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
