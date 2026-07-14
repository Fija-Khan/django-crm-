from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from contacts.models import Contact, Company
from leads.models import Lead
from deals.models import Deal
from tasks.models import Task



@login_required
def dashboard_report(request):

    # ===========================
    # Permission Based Data
    # ===========================

    if request.user.role == "admin":

        contacts = Contact.objects.all()
        companies = Company.objects.all()
        leads = Lead.objects.all()
        deals = Deal.objects.all()
        tasks = Task.objects.all()

    else:

        contacts = Contact.objects.all()

        companies = Company.objects.all()

        leads = Lead.objects.filter(
            assigned_to=request.user
        )

        deals = Deal.objects.filter(
            lead__assigned_to=request.user
        )

        tasks = Task.objects.filter(
            assigned_to=request.user
        )


    # ===========================
    # Date Filter
    # ===========================

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")


    if start_date:

        leads = leads.filter(
            created_at__date__gte=start_date
        )

        deals = deals.filter(
            created_at__date__gte=start_date
        )

        tasks = tasks.filter(
            created_at__date__gte=start_date
        )


    if end_date:

        leads = leads.filter(
            created_at__date__lte=end_date
        )

        deals = deals.filter(
            created_at__date__lte=end_date
        )

        tasks = tasks.filter(
            created_at__date__lte=end_date
        )



    # ===========================
    # Summary Cards
    # ===========================

    total_contacts = contacts.count()

    total_companies = companies.count()

    total_leads = leads.count()

    total_deals = deals.count()

    total_tasks = tasks.count()



    # ===========================
    # Deal Statistics
    # ===========================

    won_deals = deals.filter(
        stage="closed_won"
    ).count()


    lost_deals = deals.filter(
        stage="closed_lost"
    ).count()


    negotiation_deals = deals.filter(
        stage="negotiation"
    ).count()


    contract_deals = deals.filter(
        stage="contract"
    ).count()



    # ===========================
    # Revenue
    # ===========================

    total_revenue = (
        deals.filter(stage="closed_won")
        .aggregate(
            total=Sum("amount")
        )["total"] or 0
    )


# ===========================
# Monthly Revenue Report
# ===========================

    monthly_revenue = (
           deals.filter(stage="closed_won")
           .annotate(
              month=TruncMonth("created_at")
        )
         .values("month")
         .annotate(
        revenue=Sum("amount")
        )
        .order_by("month")
    )


    # ===========================
    # Recent Records
    # ===========================

    recent_leads = leads.order_by(
        "-created_at"
    )[:5]


    recent_deals = deals.order_by(
        "-created_at"
    )[:5]


    recent_tasks = tasks.order_by(
        "-created_at"
    )[:5]



    # ===========================
    # Context
    # ===========================

    context = {

        "total_contacts": total_contacts,

        "total_companies": total_companies,

        "total_leads": total_leads,

        "total_deals": total_deals,

        "total_tasks": total_tasks,


        "won_deals": won_deals,

        "lost_deals": lost_deals,

        "negotiation_deals": negotiation_deals,

        "contract_deals": contract_deals,


        "total_revenue": total_revenue,


        "recent_leads": recent_leads,

        "recent_deals": recent_deals,

        "recent_tasks": recent_tasks,


    }


    return render(
        request,
        "reports/dashboard.html",
        context
    )