# import os
# import django
from celery import shared_task
from datetime import timedelta
from django.utils import timezone

# # Set the DJANGO_SETTINGS_MODULE environment variable
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# django.setup()

from core.models import Invoice
from django.contrib.auth.models import User
from core.utils import send_email

messages = {
    "7_days": """\
            <html>
            <body>
            <p>Hi {name},</p>
            <p>I hope this email finds you well.</p>
            <p>I'm writing to remind you that a payment of <strong>{amount}</strong> GBP is due for invoice {invoice_number} on <strong>{due_date}</strong> which is in 7 days.</p>
            <p>Your prompt attention to this matter would be greatly appreciated. If there are any questions or concerns regarding the invoice or payment process, please don't hesitate to reach out to us on {company_email}.</p>
            <p>Thank you for your attention to this matter.</p>
            <p>Best regards,</p>
            <p>{company_name}</p>
            </body>
            </html>
        """,
    "5_days": """\
            <html>
            <body>
            <p>Hi {name},</p>
            <p>I hope this email finds you well.</p>
            <p>I'm writing to remind you that a payment of <strong>{amount}</strong> GBP is due for invoice {invoice_number} on <strong>{due_date}</strong> which is in 5 days.</p>
            <p>Your prompt attention to this matter would be greatly appreciated. If there are any questions or concerns regarding the invoice or payment process, please don't hesitate to reach out to us on {company_email}.</p>
            <p>Thank you for your attention to this matter.</p>
            <p>Best regards,</p>
            <p>{company_name}</p>
            </body>
            </html>
        """,
    "3_days": """\
            <html>
            <body>
            <p>Hi {name},</p>
            <p>I hope this email finds you well.</p>
            <p>I'm writing to remind you that a payment of <strong>{amount}</strong> GBP is due for invoice {invoice_number} on <strong>{due_date}</strong> which is in 3 days.</p>
            <p>Your prompt attention to this matter would be greatly appreciated. If there are any questions or concerns regarding the invoice or payment process, please don't hesitate to reach out to us on {company_email}.</p>
            <p>Thank you for your attention to this matter.</p>
            <p>Best regards,</p>
            <p>{company_name}</p>
            </body>
            </html>
        """,
    "1_day" : """\
            <html>
            <body>
            <p>Hi {name},</p>
            <p>I hope this email finds you well.</p>
            <p>I'm writing to remind you that a payment of <strong>{amount}</strong> GBP is due for invoice {invoice_number} on <strong>{due_date}</strong> which is tomorrow.</p>
            <p>Your prompt attention to this matter would be greatly appreciated. If there are any questions or concerns regarding the invoice or payment process, please don't hesitate to reach out to us on {company_email}.</p>
            <p>Thank you for your attention to this matter.</p>
            <p>Best regards,</p>
            <p>{company_name}</p>
            </body>
            </html>
        """,
    "the_due_date": """\
            <html>
            <body>
            <p>Hi {name},</p>
            <p>I hope this email finds you well.</p>
            <p>I'm writing to remind you that a payment of <strong>{amount}</strong> GBP is due for invoice {invoice_number} on <strong>{due_date}</strong> today.</p>
            <p>Your prompt attention to this matter would be greatly appreciated. If there are any questions or concerns regarding the invoice or payment process, please don't hesitate to reach out to us on {company_email}.</p>
            <p>Thank you for your attention to this matter.</p>
            <p>Best regards,</p>
            <p>{company_name}</p>
            </body>
            </html>
        """,
    "over_due_date": """\
            <html>
            <body>
            <p>Hi {name},</p>
            <p>I hope this email finds you well.</p>
            <p>I'm writing to remind you that a payment of <strong>{amount}</strong> GBP is past due for invoice {invoice_number} on <strong>{due_date}</strong>.</p>
            <p>Your prompt attention to this matter would be greatly appreciated. If there are any questions or concerns regarding the invoice or payment process, please don't hesitate to reach out to us on {company_email}.</p>
            <p>Thank you for your attention to this matter.</p>
            <p>Best regards,</p>
            <p>{company_name}</p>
            </body>
            </html>
        """
}



def get_company_email(company):
    user = User.objects.filter(username=company).first()
    user_email = user.email
    return user_email

@shared_task           
def send_7_days_reminder():
    reminder_date = timezone.now().date() + timedelta(days=7)
    invoices = Invoice.objects.filter(due_date=reminder_date, is_paid=False)
    for invoice in invoices:
        subject=f"Reminder: Upcoming Invoice Payment Due in 7 Days {invoice.invoice_number}"
        receiver_email=invoice.email
        company = invoice.company
        company_email = get_company_email(company)
        
        message = messages.get('7_days').format(
            name= invoice.name,
            amount= invoice.amount,
            invoice_number=invoice.invoice_number,
            due_date=invoice.due_date,
            company_email=company_email,
            company_name=company.username 
        )
        send_email(
            subject=subject, 
            receiver_email=receiver_email, 
            message=message, 
            company_name=str(company).capitalize(),
            company_email=company_email
        )

@shared_task       
def send_5_days_reminder():
    reminder_date = timezone.now().date() + timedelta(days=5)
    invoices = Invoice.objects.filter(due_date=reminder_date, is_paid=False)
    for invoice in invoices:
        subject=f"Reminder: Upcoming Invoice Payment Due in 5 Days {invoice.invoice_number}"
        receiver_email=invoice.email
        company = invoice.company
        company_email = get_company_email(company)
        
        message = messages.get("5_days").format(
            name= invoice.name,
            amount= invoice.amount,
            invoice_number=invoice.invoice_number,
            due_date=invoice.due_date,
            company_email=company_email,
            company_name=company.username 
        )
        send_email(
            subject=subject, 
            receiver_email=receiver_email, 
            message=message, 
            company_name=str(company).capitalize(),
            company_email=company_email
        )

@shared_task
def send_3_days_reminder():
    reminder_date = timezone.now().date() + timedelta(days=3)
    invoices = Invoice.objects.filter(due_date=reminder_date, is_paid=False)
    for invoice in invoices:
        subject=f"Reminder: Upcoming Invoice Payment Due in 3 Days {invoice.invoice_number}"
        receiver_email=invoice.email
        company = invoice.company
        company_email = get_company_email(company)
        
        message = messages.get("3_days").format(
            name= invoice.name,
            amount= invoice.amount,
            invoice_number=invoice.invoice_number,
            due_date=invoice.due_date,
            company_email=company_email,
            company_name=company.username 
        )
        send_email(
            subject=subject, 
            receiver_email=receiver_email, 
            message=message, 
            company_name=str(company).capitalize(),
            company_email=company_email
        )   

@shared_task   
def send_1_day_reminder():
    reminder_date = timezone.now().date() + timedelta(days=1)
    invoices = Invoice.objects.filter(due_date=reminder_date, is_paid=False)
    for invoice in invoices:
        subject=f"Reminder: Upcoming Invoice Payment Due in 1 Day {invoice.invoice_number}"
        receiver_email=invoice.email
        company = invoice.company
        company_email = get_company_email(company)
        
        message = messages.get("1_day").format(
            name= invoice.name,
            amount= invoice.amount,
            invoice_number=invoice.invoice_number,
            due_date=invoice.due_date,
            company_email=company_email,
            company_name=company.username 
        )
        send_email(
            subject=subject, 
            receiver_email=receiver_email, 
            message=message, 
            company_name=str(company).capitalize(),
            company_email=company_email
        )

@shared_task           
def send_due_date_reminder():
    reminder_date = timezone.now().date()
    invoices = Invoice.objects.filter(due_date=reminder_date, is_paid=False)
    for invoice in invoices:
        subject=f"Reminder: Upcoming Invoice Payment Due Today {invoice.invoice_number}"
        receiver_email=invoice.email
        company = invoice.company
        company_email = get_company_email(company)
        
        message = messages.get("the_due_date").format(
            name= invoice.name,
            amount= invoice.amount,
            invoice_number=invoice.invoice_number,
            due_date=invoice.due_date,
            company_email=company_email,
            company_name=company.username 
        )
        send_email(
            subject=subject, 
            receiver_email=receiver_email, 
            message=message, 
            company_name=str(company).capitalize(),
            company_email=company_email
        )

@shared_task           
def send_over_due_reminder():
    invoices = Invoice.objects.filter(due_date__lt=timezone.now().date(), is_paid=False)
    for invoice in invoices:
        subject=f"Reminder: Invoice Payment Over Due {invoice.invoice_number}"
        receiver_email=invoice.email
        company = invoice.company
        company_email = get_company_email(company)
        
        message = messages.get("over_due_date").format(
            name= invoice.name,
            amount= invoice.amount,
            invoice_number=invoice.invoice_number,
            due_date=invoice.due_date,
            company_email=company_email,
            company_name=company.username 
        )
        send_email(
            subject=subject, 
            receiver_email=receiver_email, 
            message=message, 
            company_name=str(company).capitalize(),
            company_email=company_email
        )
        