from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from leads.models import Lead
from contacts.models import Contact
from deals.models import Deal
from tasks.models import Task
from interactions.models import Interaction


@login_required
def dashboard_view(request):

    today = timezone.now().date()

    # =========================
    # ROLE BASED QUERY SETS
    # =========================
    if request.user.role == "admin":
        leads_qs = Lead.objects.all()
        contacts_qs = Contact.objects.all()
        deals_qs = Deal.objects.all()

        # ADMIN CAN SEE ALL TASKS
        my_tasks = Task.objects.all().order_by('due_date')

    else:
        leads_qs = Lead.objects.filter(assigned_to=request.user)
        contacts_qs = Contact.objects.filter(assigned_to=request.user)
        deals_qs = Deal.objects.filter(lead__assigned_to=request.user)

        # USER TASKS (ASSIGNED ONLY)
        my_tasks = Task.objects.filter(
            assigned_to=request.user
        ).order_by('due_date')

    # =========================
    # KPI COUNTS
    # =========================
    total_leads = leads_qs.count()
    total_contacts = contacts_qs.count()
    total_deals = deals_qs.count()

    # =========================
    # FILTER TODAY + OVERDUE TASKS (OPTIONAL DISPLAY LOGIC)
    # =========================
    pending_tasks = my_tasks.filter(
        status__iexact='pending',
        due_date__lte=today
    )

    # =========================
    # RECENT ACTIVITY
    # =========================
    recent_activities = Interaction.objects.all().order_by('-id')[:10]

    # =========================
    # CONTEXT
    # =========================
    context = {
        'total_leads': total_leads,
        'total_contacts': total_contacts,
        'total_deals': total_deals,

        # show filtered tasks in dashboard
        'my_tasks': pending_tasks,

        'recent_activities': recent_activities,
    }

    return render(request, 'dashboard/dashboard.html', context)