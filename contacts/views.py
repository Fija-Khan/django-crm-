from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Contact


@login_required
def contact_list(request):

    contacts = Contact.objects.all().order_by("-created_at")

    # Search
    search = request.GET.get("search")
    if search:
        contacts = contacts.filter(first_name__icontains=search)

    # Filter by Source
    source = request.GET.get("source")
    if source:
        contacts = contacts.filter(source=source)

    # Filter by Company
    company = request.GET.get("company")
    if company:
        contacts = contacts.filter(company_id=company)

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search": search,
        "source": source,
        "company": company,
    }

    return render(request, "contacts/contact_list.html", context)