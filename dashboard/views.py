import json

from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Max, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.utils import timezone

from accounts.models import CustomUser
from contacts.models import Company, Contact
from deals.models import Deal
from interactions.models import Interaction
from leads.models import Lead
from tasks.models import Task


@login_required
def dashboard_view(request):
    """
    CRM Dashboard

    Admin:
        Access to all CRM records

    Agent:
        Access only assigned records
    """

    today = timezone.now().date()


    # =====================================================
    # ROLE BASED DATA ACCESS
    # =====================================================

    if request.user.role == "admin":

        # -------------------------
        # Contacts
        # -------------------------

        contacts = (
            Contact.objects
            .select_related(
                "company",
                "assigned_to",
            )
        )


        # -------------------------
        # Companies
        # -------------------------

        companies = Company.objects.all()



        # -------------------------
        # Leads
        # -------------------------

        leads = (
            Lead.objects
            .select_related(
                "contact",
                "assigned_to",
            )
        )



        # -------------------------
        # Deals
        # -------------------------

        deals = (
            Deal.objects
            .select_related(
                "lead",
                "lead__contact",
            )
        )



        # -------------------------
        # Tasks
        # -------------------------

        tasks = (
            Task.objects
            .select_related(
                "assigned_to",
                "related_contact",
                "related_lead",
            )
        )



        # -------------------------
        # Interactions
        # -------------------------

        interactions = (
            Interaction.objects
            .select_related(
                "contact",
                "lead",
                "logged_by",
            )
        )



        # -------------------------
        # Agents
        # -------------------------

        agents = (
            CustomUser.objects
            .filter(
                role="agent",
                is_active=True,
                is_approved=True,
            )
        )



    else:


        # -------------------------
        # Agent Contacts
        # -------------------------

        contacts = (
            Contact.objects
            .filter(
                assigned_to=request.user
            )
            .select_related(
                "company",
                "assigned_to",
            )
        )



        # -------------------------
        # Agent Companies
        # -------------------------

        companies = (
            Company.objects
            .filter(
                contact__assigned_to=request.user
            )
            .distinct()
        )



        # -------------------------
        # Agent Leads
        # -------------------------

        leads = (
            Lead.objects
            .filter(
                assigned_to=request.user
            )
            .select_related(
                "contact",
                "assigned_to",
            )
        )



        # -------------------------
        # Agent Deals
        # -------------------------

        deals = (
            Deal.objects
            .filter(
                lead__assigned_to=request.user
            )
            .select_related(
                "lead",
                "lead__contact",
            )
        )



        # -------------------------
        # Agent Tasks
        # -------------------------

        tasks = (
            Task.objects
            .filter(
                assigned_to=request.user
            )
            .select_related(
                "assigned_to",
                "related_contact",
                "related_lead",
            )
        )



        # -------------------------
        # Agent Interactions
        # -------------------------

        interactions = (
            Interaction.objects
            .filter(
                contact__assigned_to=request.user
            )
            .select_related(
                "contact",
                "lead",
                "logged_by",
            )
        )



        # -------------------------
        # Current Agent
        # -------------------------

        agents = (
            CustomUser.objects
            .filter(
                id=request.user.id
            )
        )

    # =====================================================
    # KPI CARDS
    # =====================================================

    total_contacts = contacts.count()

    total_companies = companies.count()

    total_leads = leads.count()

    total_deals = deals.count()

    total_agents = agents.count()



    # =====================================================
    # LEAD PIPELINE STATISTICS
    # =====================================================

    lead_pipeline = (
        leads
        .values("status")
        .annotate(
            total=Count("id")
        )
        .order_by("status")
    )


    pipeline_labels = []

    pipeline_counts = []


    for item in lead_pipeline:

        pipeline_labels.append(
            item["status"].replace(
                "_",
                " "
            ).title()
        )

        pipeline_counts.append(
            item["total"]
        )



    new_leads = leads.filter(
        status="new"
    ).count()


    contacted_leads = leads.filter(
        status="contacted"
    ).count()


    qualified_leads = leads.filter(
        status="qualified"
    ).count()


    proposal_leads = leads.filter(
        status="proposal"
    ).count()


    won_leads = leads.filter(
        status="won"
    ).count()


    lost_leads = leads.filter(
        status="lost"
    ).count()



    # =====================================================
    # DEAL STATISTICS
    # =====================================================

    negotiation_deals = deals.filter(
        stage="negotiation"
    ).count()


    contract_deals = deals.filter(
        stage="contract"
    ).count()


    won_deals = deals.filter(
        stage="closed_won"
    ).count()


    lost_deals = deals.filter(
        stage="closed_lost"
    ).count()



    open_deals = deals.exclude(
        stage__in=[
            "closed_won",
            "closed_lost",
        ]
    ).count()



    # =====================================================
    # REVENUE SUMMARY
    # =====================================================

    won_deal_queryset = deals.filter(
        stage="closed_won"
    )



    total_revenue = (
        won_deal_queryset
        .aggregate(
            total=Sum("amount")
        )
        ["total"]
        or 0
    )



    average_deal = (
        won_deal_queryset
        .aggregate(
            average=Avg("amount")
        )
        ["average"]
        or 0
    )



    highest_deal = (
        won_deal_queryset
        .aggregate(
            highest=Max("amount")
        )
        ["highest"]
        or 0
    )



    # =====================================================
    # SALES WIN RATE
    # =====================================================

    closed_deals = (
        won_deals
        +
        lost_deals
    )


    win_rate = (
        round(
            (won_deals / closed_deals) * 100,
            2
        )
        if closed_deals
        else 0
    )

    # =====================================================
    # TASK STATISTICS
    # =====================================================

    pending_tasks = tasks.filter(
        status="pending"
    ).count()


    in_progress_tasks = tasks.filter(
        status="in_progress"
    ).count()


    completed_tasks = tasks.filter(
        status="done"
    ).count()



    overdue_tasks = (
        tasks
        .filter(
            due_date__lt=today
        )
        .exclude(
            status="done"
        )
        .count()
    )



    # =====================================================
    # TODAY TASKS WIDGET
    # Requirement:
    # Agent's pending tasks for today
    # =====================================================

    today_tasks = (
        tasks
        .filter(
            due_date=today
        )
        .exclude(
            status="done"
        )
        .order_by(
            "priority",
            "due_date"
        )
    )



    # =====================================================
    # UPCOMING TASKS
    # =====================================================

    upcoming_tasks = (
        tasks
        .filter(
            due_date__gt=today
        )
        .exclude(
            status="done"
        )
        .order_by(
            "due_date"
        )[:5]
    )



    # =====================================================
    # RECENT CONTACTS
    # Requirement:
    # Latest 5 contacts
    # =====================================================

    recent_contacts = (
        contacts
        .order_by(
            "-created_at"
        )[:5]
    )



    # =====================================================
    # RECENT LEADS
    # Requirement:
    # Latest 5 leads
    # =====================================================

    recent_leads = (
        leads
        .order_by(
            "-created_at"
        )[:5]
    )



    # =====================================================
    # RECENT DEALS
    # Requirement:
    # Latest 5 deals
    # =====================================================

    recent_deals = (
        deals
        .order_by(
            "-created_at"
        )[:5]
    )



    # =====================================================
    # RECENT ACTIVITIES
    # Requirement:
    # Latest 10 interactions
    # =====================================================

    recent_activities = (
        interactions
        .order_by(
            "-interaction_date"
        )[:10]
    )



    # =====================================================
    # MONTHLY REVENUE CHART
    # Requirement:
    # Chart.js Line Chart
    # Sum of closed_won deals per month
    # =====================================================

    revenue_data = (
        deals
        .filter(
            stage="closed_won"
        )
        .annotate(
            month=TruncMonth(
                "close_date"
            )
        )
        .values(
            "month"
        )
        .annotate(
            total=Sum("amount")
        )
        .order_by(
            "month"
        )
    )



    revenue_labels = []

    revenue_totals = []



    for item in revenue_data:

        if item["month"]:

            revenue_labels.append(
                item["month"].strftime(
                    "%b"
                )
            )


            revenue_totals.append(
                float(
                    item["total"]
                )
            )

    # =====================================================
    # SUMMARY DATA
    # =====================================================

    total_pending_work = (
        pending_tasks
        +
        in_progress_tasks
    )



    crm_summary = {

        "contacts": total_contacts,

        "companies": total_companies,

        "leads": total_leads,

        "deals": total_deals,

        "revenue": total_revenue,

    }



    # =====================================================
    # FINAL CONTEXT
    # =====================================================

    context = {


        # ================= KPI =================

        "total_contacts": total_contacts,

        "total_companies": total_companies,

        "total_leads": total_leads,

        "total_deals": total_deals,

        "total_agents": total_agents,



        # ================= LEADS =================

        "new_leads": new_leads,

        "contacted_leads": contacted_leads,

        "qualified_leads": qualified_leads,

        "proposal_leads": proposal_leads,

        "won_leads": won_leads,

        "lost_leads": lost_leads,



        # ================= DEALS =================

        "negotiation_deals": negotiation_deals,

        "contract_deals": contract_deals,

        "won_deals": won_deals,

        "lost_deals": lost_deals,

        "open_deals": open_deals,



        # ================= REVENUE =================

        "total_revenue": total_revenue,

        "average_deal": average_deal,

        "highest_deal": highest_deal,

        "win_rate": win_rate,



        # ================= TASKS =================

        "pending_tasks": pending_tasks,

        "in_progress_tasks": in_progress_tasks,

        "completed_tasks": completed_tasks,

        "overdue_tasks": overdue_tasks,

        "today_tasks": today_tasks,

        "upcoming_tasks": upcoming_tasks,

        "total_pending_work": total_pending_work,



        # ================= RECENT DATA =================

        "recent_contacts": recent_contacts,

        "recent_leads": recent_leads,

        "recent_deals": recent_deals,

        "recent_activities": recent_activities,



        # ================= OTHER =================

        "today": today,

        "crm_summary": crm_summary,



        # ================= CHART DATA =================

        "pipeline_labels": json.dumps(
            pipeline_labels
        ),

        "pipeline_counts": json.dumps(
            pipeline_counts
        ),


        "revenue_labels": json.dumps(
            revenue_labels
        ),

        "revenue_totals": json.dumps(
            revenue_totals
        ),

    }



    # =====================================================
    # RENDER DASHBOARD
    # =====================================================

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )


