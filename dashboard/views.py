from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth

from contacts.models import Contact
from leads.models import Lead
from deals.models import Deal
from tasks.models import Task
from interactions.models import Interaction

import json


@login_required
def dashboard_view(request):
    today = timezone.now().date()

    # ==========================================
    # ROLE-BASED QUERYSETS
    # ==========================================
    if request.user.role == "admin":

        contacts_qs = Contact.objects.all()

        leads_qs = Lead.objects.all()

        deals_qs = Deal.objects.all()

        tasks_qs = Task.objects.all()

        recent_activities = Interaction.objects.order_by(
            "-interaction_date"
        )[:10]

    else:

        contacts_qs = Contact.objects.filter(
            assigned_to=request.user
        )

        leads_qs = Lead.objects.filter(
            assigned_to=request.user
        )

        deals_qs = Deal.objects.filter(
            lead__assigned_to=request.user
        )

        tasks_qs = Task.objects.filter(
            assigned_to=request.user
        )

        recent_activities = Interaction.objects.filter(
            logged_by=request.user
        ).order_by(
            "-interaction_date"
        )[:10]

    # ==========================================
    # KPI CARDS
    # ==========================================
    total_contacts = contacts_qs.count()

    total_leads = leads_qs.count()

    won_deals = deals_qs.filter(
        stage="closed_won"
    ).count()

    # ==========================================
    # LEAD PIPELINE CHART DATA
    # ==========================================
    pipeline_data = (
        leads_qs
        .values("status")
        .annotate(total=Count("id"))
    )

    pipeline_labels = []
    pipeline_counts = []

    for item in pipeline_data:
        pipeline_labels.append(item["status"].title())
        pipeline_counts.append(item["total"])

    # ==========================================
    # MONTHLY REVENUE CHART DATA
    # ==========================================
    revenue_data = (
        deals_qs
        .filter(stage="closed_won")
        .annotate(month=TruncMonth("close_date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    revenue_labels = []
    revenue_totals = []

    for item in revenue_data:

        if item["month"]:

            revenue_labels.append(
                item["month"].strftime("%b")
            )

            revenue_totals.append(
                float(item["total"])
            )

    # ==========================================
    # TODAY'S TASKS
    # ==========================================
    my_tasks = (
        tasks_qs
        .filter(
            due_date=today
        )
        .exclude(
            status="done"
        )
        .order_by("due_date")
    )

    # ==========================================
    # CONTEXT
    # ==========================================
    context = {

        "total_contacts": total_contacts,

        "total_leads": total_leads,

        "won_deals": won_deals,

        "my_tasks": my_tasks,

        "recent_activities": recent_activities,

        "today": today,

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

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )