from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .models import Invoice
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
import json
import calendar
from django.http import QueryDict
from datetime import datetime, timedelta
from .utils import generate_invoice_pdf, get_company_name
from django.core.paginator import Paginator
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear


# Create your views here.


def home(request):
    user = request.user
    return render(request, "core/index.html", {"user": user})


@login_required(login_url="login")
def dashboard(request):
    user = request.user
    dataPoint = get_invoice_analytics(request).content.decode("utf-8")
    dataPoint = json.loads(dataPoint)
    sales_report_data = sales_report(request).content.decode("utf-8")
    sales_report_data = json.loads(sales_report_data)
    # print(sales_report_data)
    invoices_result = get_user_invoices(request)
    if invoices_result:
        json_data = invoices_result.content.decode(
            "utf-8"
        )  # Decode bytes to a JSON string
        data = json.loads(json_data)  # Parse the JSON string into a Python object
        # print(data)
        invoice_result = json.loads(
            data["invoices"]
        )  # Parse the 'invoices' field into a Python object
        page_result = data["page_obj"]  # )
        num_of_pages = data["total_pages"]
    else:
        invoice_result = []
    return render(
        request,
        "core/dashboard.html",
        {
            "user": user,
            "invoices_result": invoice_result,
            "datapoints": dataPoint,
            "page_number": page_result,
            "total_pages": num_of_pages,
            "sales_report_data": sales_report_data,
        },
    )


@login_required(login_url="login")
def invoice(request):
    return render(request, "core/invoice.html")


def register(request):
    try:
        if request.method == "POST":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect("signup")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect("signup")
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                user.save()
                messages.success(request, "Registration successful, please login.")
                return redirect("login")
    except Exception as e:
        messages.error(request, "Unexpected error occurred. Please try again later.")
        return redirect("signup")
    return render(request, "core/register.html")


def login(request):
    try:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            if not username or not password:
                messages.error(request, "Invalid username or password.")
                return redirect("login")
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, "Login successful.")
                return redirect("dashboard")

            messages.error(request, "Invalid username or password.")
            return redirect("login")

    except Exception as e:
        messages.error(request, "Unexpected error occurred. Please try again later.")
        return redirect("login")

    return render(request, "core/login.html")


@login_required(login_url="login")
def create_invoice(request):
    try:
        company = request.user
        if request.method == "POST":
            name = request.POST.get("name")
            amount = request.POST.get("amount")
            email = request.POST.get("email")
            invoice_number = request.POST.get("invoice_number")
            payment_status = request.POST.get("is_paid")
            due_date = request.POST.get("due_date")
            description = request.POST.get("description")

            if Invoice.objects.filter(
                invoice_number=invoice_number, company=company
            ).exists():
                messages.error(
                    request,
                    "This invoice number is already associated with another invoice",
                )
                return render("invoice")
            print(
                f"{amount} - {invoice_number} - {payment_status} - {name} - {email} - {due_date}"
            )

            invoice = Invoice.objects.create(
                company=company,
                name=name,
                amount=amount,
                email=email,
                description=description,
                invoice_number=invoice_number,
                is_paid=bool(int(payment_status)),
                due_date=due_date,
            )
            invoice.save()
            messages.success(request, "Invoice saved successfully.")
            return redirect("invoice")
    except Exception as e:
        print(str(e))
        messages.error(
            request, "There was an error saving your invoice. Please try again."
        )
        return redirect("invoice")


@login_required(login_url="login")
def get_user_invoices(request):
    try:
        user = request.user
        invoices = Invoice.objects.filter(company=user).order_by("-created_at")
        paginator = Paginator(invoices, 10)

        page_number = request.GET.get("page")
        if page_number:
            try:
                page_number = int(page_number)
            except ValueError:
                # If page_number is not a valid integer, default to page 1
                page_number = 1
        else:
            page_number = 1

        # print(f"Number of invoices: {len(invoices)}")
        # print(f"Number of pages: {paginator.num_pages}")
        if page_number > paginator.num_pages:
            page_number = paginator.num_pages
        elif page_number < 1:
            page_number = 1
        # print(page_number)
        page_obj = paginator.get_page(page_number)
        # print(page_obj)

        serialized_invoices = serialize("json", page_obj)
        # print(serialized_invoices)
        return JsonResponse(
            {
                "invoices": serialized_invoices,
                "page_obj": page_number,
                "total_pages": paginator.num_pages,
            }
        )

    except Exception as err:
        # Log the error for debugging purposes
        print(f"Error fetching invoices: {err}")
        return JsonResponse(
            {"error": "An error occurred while fetching invoices."}, status=500
        )


@login_required(login_url="login")
def get_invoice(request, pk):
    try:
        user = request.user
        invoice = get_object_or_404(Invoice, pk=pk, company=user)

        if request.method == "GET":
            serialized_invoice = serialize("json", [invoice])

            return JsonResponse({"invoice_data": serialized_invoice})

        elif request.method == "PATCH":
            # print(request.body)
            data = QueryDict(request.body)

            email = data.get("email")
            name = data.get("name")
            amount = data.get("amount")
            invoice_number = data.get("invoice_number")
            payment_status = data.get("is_paid")
            due_date = datetime.strptime(data.get("due_date"), "%Y-%m-%d")

            # print(request.POST)
            # print(email,'....', name, '....', amount, '....', payment_status, '....', due_date)

            invoice.email = email
            invoice.name = name
            invoice.amount = amount
            invoice.is_paid = payment_status
            invoice.due_date = due_date.date()
            invoice.invoice_number = invoice_number
            invoice.save()

            messages.success(request, "Invoice details have been updated successfully")
            # serialized_invoice = serialize('json', [invoice])
            return redirect("dashboard")

    except Exception as err:
        # print(str(err))
        messages.error(request, "An unexpected error occurred. Please try again")
        return render(request, "core/dashboard.html", {"invoice": []})


def logout_view(request):
    user = request.user
    if user is not None:
        logout(request)
        messages.success(request, "You have logged out successfully")
        return render(request, "core/login.html")
    else:
        messages.error(request, "You are not logged in to any account yet.")
        return render(request, "core/login.html")


@login_required(login_url="login")
def generate_invoice(request, pk):
    try:
        user = request.user
        invoice = get_object_or_404(Invoice, pk=pk, company=user)
        serialized_invoice = serialize("json", [invoice])
        invoice_data = json.loads(serialized_invoice)[0]["fields"]
        # print(serialized_invoice)

        description = invoice_data["description"]
        total = invoice_data["amount"]
        customer_name = invoice_data["name"]
        company_name = get_company_name(invoice_data["company"]).capitalize()
        invoice_number = invoice_data["invoice_number"]
        date = invoice_data["due_date"]
        payment_status = "Paid" if invoice_data["is_paid"] == True else "Unpaid"

        generate_invoice_pdf(
            description,
            total,
            customer_name,
            invoice_number,
            date,
            company_name,
            payment_status,
        )

        messages.success(request, "Download successful")
        return redirect("dashboard")

    except Exception as e:
        # print(str(e))
        messages.error(request, "Error generating invoice")
        return redirect("dashboard")


@login_required(login_url="login")
def get_invoice_analytics(request):
    try:
        user = request.user
        paid_invoices_count = Invoice.objects.filter(company=user, is_paid=True).count()
        unpaid_invoices_count = Invoice.objects.filter(
            company=user, is_paid=False
        ).count()

        data = {
            "paid_invoices_count": paid_invoices_count,
            "unpaid_invoices_count": unpaid_invoices_count,
        }

        return JsonResponse(data)

    except Exception as e:
        data = {"paid_invoices_count": 0, "unpaid_invoices_count": 0}

        return JsonResponse(data)


@login_required(login_url="login")
def sales_report(request):
    try:
        user = request.user
        sales_data = (
            Invoice.objects.filter(company=user)
            .annotate(month=ExtractMonth("due_date"), year=ExtractYear("due_date"))
            .values("year", "month")
            .annotate(total_sales=Sum("amount"))
            .order_by("year", "month")
        )

        sales_per_month = {}
        for record in sales_data:
            year = record["year"]
            month = record["month"]
            month_name = calendar.month_name[month]
            total_sales = record["total_sales"]

            if year not in sales_per_month:
                sales_per_month[year] = {}

            sales_per_month[year][month_name] = total_sales

        return JsonResponse({"sales_per_month": sales_per_month})

    except Exception as e:
        return JsonResponse({"error": str(e)})
