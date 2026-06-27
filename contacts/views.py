import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages

from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

from .models import Contact, Company
from .forms import ContactForm


# =========================
# CONTACT LIST (IMPROVED)
# =========================
@login_required
def contact_list(request):

    contacts = Contact.objects.select_related('company').all().order_by("-created_at")

    # 🔍 SEARCH (improved)
    search = request.GET.get("search")
    if search:
        contacts = contacts.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )

    # 🎯 SOURCE FILTER
    source = request.GET.get("source")
    if source:
        contacts = contacts.filter(source=source)

    # 🏢 COMPANY FILTER
    company = request.GET.get("company")
    if company:
        contacts = contacts.filter(company_id=company)

    # 📄 PAGINATION
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search": search,
        "source": source,
        "company": company,
        "companies": Company.objects.all(),   # IMPORTANT for dropdown
    }

    return render(request, "contacts/contact_list.html", context)


# =========================
# CREATE CONTACT
# =========================
class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    success_url = reverse_lazy("contact_list")


# =========================
# CONTACT DETAIL
# =========================
class ContactDetailView(DetailView):
    model = Contact
    template_name = "contacts/contact_detail.html"
    context_object_name = "contact"


# =========================
# UPDATE CONTACT
# =========================
class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    success_url = reverse_lazy("contact_list")


# =========================
# DELETE CONTACT
# =========================
class ContactDeleteView(DeleteView):
    model = Contact
    template_name = "contacts/contact_confirm_delete.html"
    success_url = reverse_lazy("contact_list")
    
    
@login_required
def contact_import(request):

    if request.method == "POST":
        csv_file = request.FILES.get("file")

        if not csv_file:
            messages.error(request, "No file uploaded")
            return redirect("contact_list")

        if not csv_file.name.endswith(".csv"):
            messages.error(request, "Only CSV file allowed")
            return redirect("contact_list")

        file_data = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(file_data)

        created_count = 0
        skipped_count = 0

        # CSV duplicate tracking
        seen_emails = set()

        for row in reader:
            email = (row.get("Email") or "").strip().lower()

            if not email:
                skipped_count += 1
                continue

            # CSV duplicate check
            if email in seen_emails:
                skipped_count += 1
                continue

            seen_emails.add(email)

            # DB duplicate check
            if Contact.objects.filter(email=email).exists():
                skipped_count += 1
                continue

            try:
                company = None
                company_name = (row.get("Company") or "").strip()

                if company_name:
                    company, _ = Company.objects.get_or_create(name=company_name)

                Contact.objects.create(
                    first_name=row.get("First Name", "").strip(),
                    last_name=row.get("Last Name", "").strip(),
                    email=email,
                    phone=row.get("Phone", "").strip(),
                    company=company
                )

                created_count += 1

            except Exception as e:
                skipped_count += 1
                continue

        messages.success(
            request,
            f"Import completed! Created: {created_count}, Skipped: {skipped_count}"
        )
        return redirect("contact_list")

    return render(request, "contacts/contact_import.html")
    
@login_required
def contact_export(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Email', 'Phone', 'Company'])

    contacts = Contact.objects.all()

    for contact in contacts:
        writer.writerow([
            contact.first_name,
            contact.last_name,
            contact.email,
            contact.phone,
            contact.company.name if contact.company else ''
        ])

    return response