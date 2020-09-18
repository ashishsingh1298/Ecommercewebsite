from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name='ShopHome'),
    path('about/',views.about,name='AboutUs'),
    path('allproducts/',views.allproducts,name='AllProducts'),
    path('shipping_policy/',views.shipping_policy,name='ShippingPolicy'),
    path('return_policy/',views.return_policy,name='ReturnPolicy'),
    path('privacy_policy/',views.privacy_policy,name='PrivacyPolicy'),
    path('terms_of_service/',views.terms_of_service,name='TermsOfService'),
    path('tracker/',views.tracker,name='TrackingStatus'),
    path('search/',views.search,name='Search'),
    path('contact/',views.contact,name='Contact'),
    path('prodComment',views.prodComment,name='prodComment'),
    path('products/<int:myid>',views.productView,name='ProductView'),
    path('cart/',views.cart,name='Cart'),
    path('checkout/',views.checkout,name='CheckOut'),
    path('getorderid/',views.getorderid,name='GetorderStatus'),
    
    # API's
    path('profile/',views.profile,name="profile"),
    path('signup/',views.handleSignup,name="handleSignup"),
    path('login/',views.handleLogin,name="handleLogin"),
    path('logout/',views.handleLogout,name="handleLogout"),
    path('handlerequest/',views.handlerequest,name="handleRequest"),
   
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='shop/password_change.html'), 
        name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='shop/password_change_done.html'), 
        name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='shop/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='shop/password_reset_done.html'), name='password_reset_done'),
    path('password_reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='shop/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='shop/password_reset_complete.html'), name='password_reset_complete'),
]