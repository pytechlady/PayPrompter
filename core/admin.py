from django.contrib import admin
from .models import Invoice

# Register your models here.

class InvoiceManager(admin.ModelAdmin):
    list_display = ['id', 'company', 'name', 'invoice_number', 'amount', 'due_date', 'is_paid']
    
admin.site.register(Invoice, InvoiceManager)