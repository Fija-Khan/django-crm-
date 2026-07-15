from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, Avg
from django.db.models.functions import TruncMonth

from contacts.models import Contact, Company
from leads.models import Lead
from deals.models import Deal
from tasks.models import Task



@login_required
def dashboard_report(request):

    user = request.user


    # ===========================
    # Permission Based Data
    # ===========================

    if user.role == "admin":

        contacts = Contact.objects.all()

        companies = Company.objects.all()

        leads = Lead.objects.all()

        deals = Deal.objects.all()

        tasks = Task.objects.all()


    else:

        # Contact and Company
        # do not have assigned user fields

        contacts = Contact.objects.all()

        companies = Company.objects.all()


        leads = Lead.objects.filter(
            assigned_to=user
        )


        deals = Deal.objects.filter(
            lead__assigned_to=user
        )


        tasks = Task.objects.filter(
            assigned_to=user
        )



    # ===========================
    # Date Filter
    # ===========================

    start_date = request.GET.get(
        "start_date"
    )

    end_date = request.GET.get(
        "end_date"
    )


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



    open_deals = deals.exclude(
        stage__in=[
            "closed_won",
            "closed_lost"
        ]
    ).count()



    # ===========================
    # Revenue Analytics
    # ===========================


    total_revenue = (

        deals.filter(
            stage="closed_won"
        )
        .aggregate(
            total=Sum("amount")
        )
        ["total"] or 0

    )



    average_deal_value = (

        deals.aggregate(
            avg=Avg("amount")
        )
        ["avg"] or 0

    )



    # ===========================
    # Monthly Revenue Chart
    # ===========================


    monthly_revenue = (

        deals.filter(
            stage="closed_won"
        )
        .annotate(
            month=TruncMonth(
                "created_at"
            )
        )
        .values(
            "month"
        )
        .annotate(
            revenue=Sum("amount")
        )
        .order_by(
            "month"
        )

    )



    revenue_labels = []

    revenue_values = []



    for item in monthly_revenue:

        if item["month"]:

            revenue_labels.append(
                item["month"].strftime(
                    "%b %Y"
                )
            )


            revenue_values.append(
                float(
                    item["revenue"]
                )
            )



    # ===========================
    # Recent Records
    # ===========================


    recent_leads = (

        leads
        .select_related(
            "assigned_to",
            "contact"
        )
        .order_by(
            "-created_at"
        )[:5]

    )



    recent_deals = (

        deals
        .select_related(
            "lead"
        )
        .order_by(
            "-created_at"
        )[:5]

    )



    recent_tasks = (

        tasks
        .select_related(
            "assigned_to"
        )
        .order_by(
            "-created_at"
        )[:5]

    )



    # ===========================
    # Context
    # ===========================

    context = {


        # Summary Cards

        "total_contacts": total_contacts,

        "total_companies": total_companies,

        "total_leads": total_leads,

        "total_deals": total_deals,

        "total_tasks": total_tasks,



        # Deal Statistics

        "won_deals": won_deals,

        "lost_deals": lost_deals,

        "negotiation_deals": negotiation_deals,

        "contract_deals": contract_deals,

        "open_deals": open_deals,



        # Revenue

        "total_revenue": total_revenue,

        "average_deal_value": average_deal_value,



        # Chart Data

        "revenue_labels": revenue_labels,

        "revenue_values": revenue_values,



        # Recent Data

        "recent_leads": recent_leads,

        "recent_deals": recent_deals,

        "recent_tasks": recent_tasks,



        # Filters

        "start_date": start_date,

        "end_date": end_date,


    }



    return render(
        request,
        "reports/dashboard.html",
        context
    )