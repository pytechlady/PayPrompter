from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.register, name='signup'),
    path('login', views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('invoice', views.invoice, name='invoice'),
    path('create_invoice', views.create_invoice, name='create_invoice'),
    path('invoices', views.get_user_invoices, name='get_user_invoices'),
    path('invoice/<int:pk>', views.get_invoice, name='get_invoice'),
    path('logout', views.logout_view, name='logout'),
    path('invoice_file/<int:pk>', views.generate_invoice, name='generate_invoice'),
    path('invoice_analytics', views.get_invoice_analytics, name="invoice_analytics"),
]