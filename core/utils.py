import os
from pathlib import Path
from .models import User
import smtplib
from django.http import HttpResponse
from email.message import EmailMessage
from email.utils import formataddr
from decouple import config
from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph


def get_company_name(company_id):
    user = User.objects.filter(pk=company_id).first()
    user_name = user.username
    return user_name

EMAIL_SERVER = config('EMAIL_SERVER')
PORT = config('PORT')


sender_email = config('SENDER_EMAIL')
sender_password = config('SENDER_PASSWORD')


def send_email(
    subject,
    receiver_email,
    message,
    company_name,
    company_email,
):

    msg = EmailMessage()
    msg["subject"] = subject
    msg["from"] = formataddr((company_name, f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = company_email

    msg.add_alternative(
        message,
        subtype="html",
    )

    try:
        with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Email sent successfully")
    except Exception as e:
        print(f"Error: {e}")

def generate_invoice_pdf(description, total, customer_name, invoice_number, date, company_name, payment_status):
    file_name = f"{invoice_number}.pdf"
    desktop_dir = Path.home() / "Desktop"
    
    desktop_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = desktop_dir / file_name
    
    # styles = getSampleStyleSheet()
    
    doc = SimpleDocTemplate(str(file_path))
    # company_image = company_name.upper()
    flowable = []
    # flowable.append(Paragraph(company_image))
    # flowable.append(Spacer(12,12))
    flowable.append(Paragraph(f"Company Name: {company_name}"))
    flowable.append(Paragraph(f"Customer name: {customer_name}"))
    flowable.append(Paragraph(f"Payment Date: {date}"))
    flowable.append(Paragraph(f"Payment Status: {payment_status}"))
    flowable.append(Spacer(15,15))

    table_data= [['Description', 'Invoice Number', 'Amount (£)'],
                [description, invoice_number, total]]


    t = Table(table_data)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    flowable.append(t)
    flowable.append(Spacer(12,12))

    flowable.append(Paragraph(f"Total payment: £{total}"))

    doc.build(flowable)
