from django.contrib import auth
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.urls import path
from django.utils.translation import templatize
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import pay,pay_success


urlpatterns = [
    path('', views.ProductView.as_view(), name='home'),

    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),

    # path('product-detail/<int:pk>/<str:sk>', views.ProductDetailViewNew, name='product-detail-new'),


    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),

    path('cart/', views.show_cart, name='show-cart'),

    path('plus-cart/', views.plus_cart, name='plus-cart'),

    path('minus-cart/', views.minus_cart, name='minus-cart'),

    path('remove-cart/', views.remove_cart, name='remove-cart'),
    
    path('profile/', views.ProfileView.as_view(), name='profile'),

    path('address/', views.address, name='address'),

    path('orders/', views.orders, name='orders'),


    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=MyPasswordChangeForm ,success_url='/passwordchangedone/'), name='changepassword'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),

    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),

    path('meat/', views.meat, name='meat'),
    path('meat/<slug:data>', views.meat, name='meatdata'),

    path('fruit/', views.fruit, name='fruit'),
    path('fruit/<slug:data>', views.fruit, name='fruitdata'),

    path('veg/', views.veg, name='veg'),
    path('veg/<slug:data>', views.veg, name='vegdata'),

    
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'),name='logout'),


    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),


    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),


    path('checkout/', views.checkout, name='checkout'),

    path('error/', views.errorpage, name='error'),

    path('paymentdone/', views.payment_done, name='paymentdone'),

    path('shipping/', views.shipping, name='shipping'),

    path('pay/', views.pay, name='pay'),
    
    path('pay-success/', views.pay_success, name='pay-success'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


