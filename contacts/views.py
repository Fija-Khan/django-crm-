import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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

from accounts.models import CustomUser
from .forms import ContactForm, CompanyForm
from .models import Contact, Company


# ==========================================
# CONTACT LIST
# ==========================================

@login_required
def contact_list(request):

    user = request.user

    # -----------------------------
    # Base Query
    # -----------------------------

    if user.role == "admin":
        contacts = Contact.objects.select_related(
            "company",
            "assigned_to",
        )

    else:
        contacts = Contact.objects.select_related(
            "company",
            "assigned_to",
        ).filter(
            assigned_to=user
        )

    # -----------------------------
    # Search
    # -----------------------------

    search = request.GET.get("search", "").strip()

    if search:
        contacts = contacts.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(email__icontains=search)
            | Q(phone__icontains=search)
        )

    # -----------------------------
    # Source Filter
    # -----------------------------

    source = request.GET.get("source", "").strip()

    if source:
        contacts = contacts.filter(source=source)

    # -----------------------------
    # Company Filter
    # -----------------------------

    company = request.GET.get("company", "").strip()

    if company:
        contacts = contacts.filter(company_id=company)

    # -----------------------------
    # Ordering
    # -----------------------------

    contacts = contacts.order_by("-created_at")

    # -----------------------------
    # Pagination
    # -----------------------------

    paginator = Paginator(contacts, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "search": search,
        "source": source,
        "company": company,
        "companies": Company.objects.order_by("name"),
    }

    return render(
        request,
        "contacts/contact_list.html",
        context,
    )
# ==========================================
# CREATE CONTACT
# ==========================================

class ContactCreateView(
    LoginRequiredMixin,
    CreateView,
):

    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    success_url = reverse_lazy("contacts:contact_list")

    def get_form(self, form_class=None):

        form = super().get_form(form_class)

        # Agent cannot assign contacts to others
        if self.request.user.role == "agent":
            form.fields["assigned_to"].disabled = True

        # Admin can assign only approved agents
        elif "assigned_to" in form.fields:
            form.fields["assigned_to"].queryset = CustomUser.objects.filter(
                role="agent",
                is_approved=True,
            ).order_by("first_name", "username")

        return form

    def form_valid(self, form):

        # Automatically assign contact to logged-in agent
        if self.request.user.role == "agent":
            form.instance.assigned_to = self.request.user

        messages.success(
            self.request,
            "Contact created successfully."
        )

        return super().form_valid(form)


# ==========================================
# CONTACT DETAIL
# ==========================================

class ContactDetailView(
    LoginRequiredMixin,
    DetailView,
):

    model = Contact
    template_name = "contacts/contact_detail.html"
    context_object_name = "contact"

    def get_queryset(self):

        user = self.request.user

        queryset = Contact.objects.select_related(
            "company",
            "assigned_to",
        )

        if user.role == "admin":
            return queryset

        return queryset.filter(
            assigned_to=user
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        contact = self.object

        # Related Data
        context["leads"] = contact.lead_set.all()
        context["notes"] = contact.notes.all()
        context["interactions"] = contact.interactions.all()   
        return context
# ==========================================
# UPDATE CONTACT
# ==========================================

class ContactUpdateView(
    LoginRequiredMixin,
    UpdateView,
):

    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    success_url = reverse_lazy("contacts:contact_list")

    def get_queryset(self):

        user = self.request.user

        queryset = Contact.objects.select_related(
            "company",
            "assigned_to",
        )

        if user.role == "admin":
            return queryset

        return queryset.filter(
            assigned_to=user
        )

    def get_form(self, form_class=None):

        form = super().get_form(form_class)

        # Agent cannot change assigned agent
        if self.request.user.role == "agent":
            form.fields["assigned_to"].disabled = True

        # Admin can assign only approved agents
        elif "assigned_to" in form.fields:
            form.fields["assigned_to"].queryset = CustomUser.objects.filter(
                role="agent",
                is_approved=True,
            ).order_by("first_name", "username")

        return form

    def form_valid(self, form):

        # Prevent agents from changing assignment
        if self.request.user.role == "agent":
            form.instance.assigned_to = self.request.user

        messages.success(
            self.request,
            "Contact updated successfully."
        )

        return super().form_valid(form)


# ==========================================
# DELETE CONTACT
# ==========================================

class ContactDeleteView(
    LoginRequiredMixin,
    DeleteView,
):

    model = Contact
    template_name = "contacts/contact_confirm_delete.html"
    success_url = reverse_lazy("contacts:contact_list")

    def get_queryset(self):

        user = self.request.user

        queryset = Contact.objects.select_related(
            "company",
            "assigned_to",
        )

        if user.role == "admin":
            return queryset

        return queryset.filter(
            assigned_to=user
        )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Contact deleted successfully."
        )

        return super().form_valid(form)
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
                "Please upload a CSV file."
            )
            return redirect("contacts:contact_import")

        if not csv_file.name.lower().endswith(".csv"):
            messages.error(
                request,
                "Only CSV files are allowed."
            )
            return redirect("contacts:contact_import")

        try:

            reader = csv.DictReader(
                csv_file.read().decode("utf-8").splitlines()
            )

            created = 0
            skipped = 0

            valid_sources = [
                "website",
                "referral",
                "social",
                "cold_call",
            ]

            for row in reader:

                email = row.get(
                    "Email",
                    ""
                ).strip().lower()

                if not email:
                    skipped += 1
                    continue

                if Contact.objects.filter(email=email).exists():
                    skipped += 1
                    continue

                # -------------------------
                # Company
                # -------------------------

                company = None

                company_name = row.get(
                    "Company",
                    ""
                ).strip()

                if company_name:
                    company, _ = Company.objects.get_or_create(
                        name=company_name
                    )

                # -------------------------
                # Source
                # -------------------------

                source = row.get(
                    "Source",
                    "website"
                ).strip().lower()

                if source not in valid_sources:
                    source = "website"

                # -------------------------
                # Assigned User
                # -------------------------

                assigned_user = None

                if request.user.role == "agent":

                    assigned_user = request.user

                else:

                    username = row.get(
                        "Assigned To",
                        ""
                    ).strip()

                    if username:

                        assigned_user = CustomUser.objects.filter(
                            username=username,
                            role="agent",
                            is_approved=True,
                        ).first()

                # -------------------------
                # Create Contact
                # -------------------------

                Contact.objects.create(
                    first_name=row.get(
                        "First Name",
                        ""
                    ).strip(),

                    last_name=row.get(
                        "Last Name",
                        ""
                    ).strip(),

                    email=email,

                    phone=row.get(
                        "Phone",
                        ""
                    ).strip(),

                    company=company,
                    assigned_to=assigned_user,
                    source=source,
                )

                created += 1

            messages.success(
                request,
                f"{created} contacts imported successfully. {skipped} skipped."
            )

        except Exception as e:

            messages.error(
                request,
                f"Import failed: {e}"
            )

        return redirect("contacts:contact_list")

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

    writer.writerow([
        "First Name",
        "Last Name",
        "Email",
        "Phone",
        "Company",
        "Assigned To",
        "Source",
        "Created At",
    ])

    user = request.user

    if user.role == "admin":

        contacts = Contact.objects.select_related(
            "company",
            "assigned_to",
        ).order_by("-created_at")

    else:

        contacts = Contact.objects.select_related(
            "company",
            "assigned_to",
        ).filter(
            assigned_to=user
        ).order_by("-created_at")

    for contact in contacts:

        writer.writerow([
            contact.first_name,
            contact.last_name,
            contact.email,
            contact.phone,
            contact.company.name if contact.company else "",
            contact.assigned_to.get_full_name()
            if contact.assigned_to and contact.assigned_to.get_full_name()
            else (
                contact.assigned_to.username
                if contact.assigned_to
                else ""
            ),
            contact.get_source_display(),
            contact.created_at.strftime("%d-%m-%Y %H:%M"),
        ])

    return response


# ==========================================
# COMPANY LIST
# ==========================================

@login_required
def company_list(request):

    companies = Company.objects.all().order_by("name")

    search = request.GET.get(
        "search",
        ""
    ).strip()

    if search:

        companies = companies.filter(
            Q(name__icontains=search) |
            Q(industry__icontains=search)
        )

    paginator = Paginator(
        companies,
        10
    )

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    context = {
        "page_obj": page_obj,
        "search": search,
    }

    return render(
        request,
        "contacts/company_list.html",
        context,
    )
# ==========================================
# CREATE COMPANY
# ==========================================

class CompanyCreateView(
    LoginRequiredMixin,
    CreateView,
):

    model = Company
    form_class = CompanyForm
    template_name = "contacts/company_form.html"
    success_url = reverse_lazy("contacts:company_list")

    def form_valid(self, form):

        messages.success(
            self.request,
            "Company created successfully."
        )

        return super().form_valid(form)


# ==========================================
# COMPANY DETAIL
# ==========================================

class CompanyDetailView(
    LoginRequiredMixin,
    DetailView,
):

    model = Company
    template_name = "contacts/company_detail.html"
    context_object_name = "company"

    def get_queryset(self):

        return Company.objects.prefetch_related(
            "contact_set"
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["contacts"] = Contact.objects.filter(
            company=self.object
        ).select_related(
            "assigned_to"
        ).order_by(
            "-created_at"
        )

        return context
# ==========================================
# UPDATE COMPANY
# ==========================================

class CompanyUpdateView(
    LoginRequiredMixin,
    UpdateView,
):

    model = Company
    form_class = CompanyForm
    template_name = "contacts/company_form.html"
    success_url = reverse_lazy("contacts:company_list")

    def form_valid(self, form):

        messages.success(
            self.request,
            "Company updated successfully."
        )

        return super().form_valid(form)


# ==========================================
# DELETE COMPANY
# ==========================================

class CompanyDeleteView(
    LoginRequiredMixin,
    DeleteView,
):

    model = Company
    template_name = "contacts/company_confirm_delete.html"
    success_url = reverse_lazy("contacts:company_list")

    def delete(self, request, *args, **kwargs):

        messages.success(
            request,
            "Company deleted successfully."
        )

        return super().delete(
            request,
            *args,
            **kwargs
        )
