import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .forms import ContactForm
from .models import Contact, Company


# ==========================================
# CONTACT LIST
# ==========================================

@login_required
def contact_list(request):

    contacts = (
        Contact.objects
        .select_related("company")
        .all()
        .order_by("-created_at")
    )

    # Search
    search = request.GET.get("search")

    if search:
        contacts = contacts.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(email__icontains=search)
            | Q(phone__icontains=search)
        )

    # Source Filter
    source = request.GET.get("source")

    if source:
        contacts = contacts.filter(source=source)

    # Company Filter
    company = request.GET.get("company")

    if company:
        contacts = contacts.filter(company_id=company)

    # Pagination
    paginator = Paginator(contacts, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search": search,
        "source": source,
        "company": company,
        "companies": Company.objects.all(),
    }

    return render(
        request,
        "contacts/contact_list.html",
        context,
    )


# ==========================================
# CREATE CONTACT
# ==========================================

class ContactCreateView(CreateView):

    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    success_url = reverse_lazy("contact_list")

    def form_valid(self, form):

        messages.success(
            self.request,
            "Contact created successfully."
        )

        return super().form_valid(form)

    def form_invalid(self, form):

        messages.error(
            self.request,
            "Please correct the errors below."
        )

        return super().form_invalid(form)
    
# ==========================================
# CONTACT DETAIL
# ==========================================

class ContactDetailView(DetailView):

    model = Contact
    template_name = "contacts/contact_detail.html"
    context_object_name = "contact"


# ==========================================
# UPDATE CONTACT
# ==========================================

class ContactUpdateView(UpdateView):

    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    success_url = reverse_lazy("contact_list")

    def form_valid(self, form):

        messages.success(
            self.request,
            "Contact updated successfully."
        )

        return super().form_valid(form)

    def form_invalid(self, form):

        messages.error(
            self.request,
            "Please correct the errors below."
        )

        return super().form_invalid(form)


# ==========================================
# DELETE CONTACT
# ==========================================

# ==========================================
# DELETE CONTACT
# ==========================================

class ContactDeleteView(DeleteView):

    model = Contact
    template_name = "contacts/contact_confirm_delete.html"
    success_url = reverse_lazy("contact_list")

    def delete(self, request, *args, **kwargs):

        messages.success(
            request,
            "Contact deleted successfully."
        )

        return super().delete(request, *args, **kwargs)
    
# ==========================================
# IMPORT CONTACTS
# ==========================================

@login_required
def contact_import(request):

    if request.method == "POST":

        csv_file = request.FILES.get("file")

        if not csv_file:

            messages.error(
                request,
                "No file uploaded."
            )

            return redirect("contact_list")

        if not csv_file.name.endswith(".csv"):

            messages.error(
                request,
                "Only CSV files are allowed."
            )

            return redirect("contact_list")

        file_data = csv_file.read().decode("utf-8").splitlines()

        reader = csv.DictReader(file_data)

        created_count = 0
        skipped_count = 0

        seen_emails = set()

        for row in reader:

            email = (
                row.get("Email") or ""
            ).strip().lower()

            if not email:
                skipped_count += 1
                continue

            if email in seen_emails:
                skipped_count += 1
                continue

            seen_emails.add(email)

            if Contact.objects.filter(email=email).exists():
                skipped_count += 1
                continue

            try:

                company = None

                company_name = (
                    row.get("Company") or ""
                ).strip()

                if company_name:

                    company, _ = Company.objects.get_or_create(
                        name=company_name
                    )

                Contact.objects.create(
                    first_name=row.get("First Name", "").strip(),
                    last_name=row.get("Last Name", "").strip(),
                    email=email,
                    phone=row.get("Phone", "").strip(),
                    company=company,
                )

                created_count += 1

            except Exception:
                skipped_count += 1

        messages.success(
            request,
            f"Import completed successfully! "
            f"Created: {created_count}, "
            f"Skipped: {skipped_count}"
        )

        return redirect("contact_list")

    return render(
        request,
        "contacts/contact_import.html",
    )


# ==========================================
# EXPORT CONTACTS
# ==========================================

@login_required
def contact_export(request):

    response = HttpResponse(
        content_type="text/csv"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="contacts.csv"'

    writer = csv.writer(response)

    writer.writerow(
        [
            "First Name",
            "Last Name",
            "Email",
            "Phone",
            "Company",
        ]
    )

    contacts = Contact.objects.select_related(
        "company"
    ).all()

    for contact in contacts:

        writer.writerow(
            [
                contact.first_name,
                contact.last_name,
                contact.email,
                contact.phone,
                contact.company.name if contact.company else "",
            ]
        )

    return response