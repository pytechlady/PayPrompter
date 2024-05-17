from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Invoice(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoice')
    name = models.CharField(max_length=250)
    email = models.EmailField()
    invoice_number = models.CharField(max_length=30, unique=True)
    description = models.TextField(default='For item purchased')
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    due_date = models.DateField(null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.company} - {self.name} - {self.invoice_number} - {self.amount}"
    
    