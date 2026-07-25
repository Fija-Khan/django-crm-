from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from django.contrib.auth import get_user_model

from .forms import LeadForm
from .models import Lead

from deals.models import Deal


User = get_user_model()



# ==================================================
# HELPER
# ==================================================

def get_user_leads(user):

    if user.role == "admin":
        return Lead.objects.all()

    return Lead.objects.filter(
        assigned_to=user
    )



# ==================================================
# LEAD LIST
# ==================================================

@login_required
def lead_list(request):

    leads = (
        get_user_leads(request.user)
        .select_related(
            "contact",
            "assigned_to"
        )
        .order_by("-created_at")
    )


    search = request.GET.get("search")

    if search:
        leads = leads.filter(
            title__icontains=search
        )


    status = request.GET.get("status")

    if status:
        leads = leads.filter(
            status=status
        )


    agent = request.GET.get("agent")

    if agent and request.user.role == "admin":

        leads = leads.filter(
            assigned_to_id=agent
        )


    paginator = Paginator(
        leads,
        10
    )

    page_obj = paginator.get_page(
        request.GET.get("page")
    )


    context = {

        "leads":page_obj,
        "page_obj":page_obj,

        "status_choices":
            Lead.STATUS_CHOICES,

        "agents":
            User.objects.filter(
                role="agent"
            )
    }


    return render(
        request,
        "leads/lead_list.html",
        context
    )



# ==================================================
# CREATE LEAD
# ==================================================

@login_required
def lead_add(request):

    if request.method == "POST":

        form = LeadForm(
            request.POST
        )


        if form.is_valid():

            lead = form.save(
                commit=False
            )


            if request.user.role != "admin":

                lead.assigned_to = request.user


            lead.save()


            messages.success(
                request,
                "Lead created successfully."
            )


            return redirect(
                "leads:lead_detail",
                pk=lead.pk
            )


    else:

        form = LeadForm()



    return render(
        request,
        "leads/lead_form.html",
        {
            "form":form
        }
    )



# ==================================================
# DETAIL
# ==================================================

@login_required
def lead_detail(request,pk):

    lead = get_object_or_404(

        Lead.objects
        .select_related(
            "contact",
            "assigned_to"
        )
        .prefetch_related(
            "activities",
            "interactions",
            "notes"
        ),

        pk=pk
    )


    if request.user.role != "admin":

        if lead.assigned_to != request.user:

            messages.error(
                request,
                "Permission denied."
            )

            return redirect(
                "leads:lead_list"
            )



    return render(
        request,
        "leads/lead_detail.html",
        {
            "lead":lead
        }
    )



# ==================================================
# EDIT
# ==================================================

@login_required
def lead_edit(request,pk):

    lead=get_object_or_404(
        Lead,
        pk=pk
    )


    if request.user.role!="admin":

        if lead.assigned_to != request.user:

            messages.error(
                request,
                "Permission denied."
            )

            return redirect(
                "leads:lead_list"
            )



    if request.method=="POST":

        form=LeadForm(
            request.POST,
            instance=lead
        )


        if form.is_valid():

            updated=form.save(
                commit=False
            )


            if request.user.role!="admin":

                updated.assigned_to=request.user


            updated.save()


            messages.success(
                request,
                "Lead updated successfully."
            )


            return redirect(
                "leads:lead_detail",
                pk=lead.pk
            )


    else:

        form=LeadForm(
            instance=lead
        )



    return render(
        request,
        "leads/lead_form.html",
        {
            "form":form,
            "lead":lead
        }
    )



# ==================================================
# DELETE
# ==================================================

@login_required
def lead_delete(request,pk):

    lead=get_object_or_404(
        Lead,
        pk=pk
    )


    if request.user.role!="admin":

        if lead.assigned_to != request.user:

            messages.error(
                request,
                "Permission denied."
            )

            return redirect(
                "leads:lead_list"
            )



    if request.method=="POST":

        lead.delete()


        messages.success(
            request,
            "Lead deleted successfully."
        )


        return redirect(
            "leads:lead_list"
        )



    return render(
        request,
        "leads/lead_confirm_delete.html",
        {
            "lead":lead
        }
    )



# ==================================================
# KANBAN
# ==================================================

@login_required
def lead_kanban(request):

    leads=get_user_leads(
        request.user
    )


    context={

        "new_leads":
            leads.filter(status="new"),

        "contacted_leads":
            leads.filter(status="contacted"),

        "qualified_leads":
            leads.filter(status="qualified"),

        "proposal_leads":
            leads.filter(status="proposal"),

        "won_leads":
            leads.filter(status="won"),

        "lost_leads":
            leads.filter(status="lost"),

    }


    return render(
        request,
        "leads/lead_kanban.html",
        context
    )



# ==================================================
# AJAX STAGE UPDATE
# ==================================================

@login_required
@require_POST
def update_stage(request):

    lead_id=request.POST.get(
        "lead_id"
    )

    status=request.POST.get(
        "status"
    )


    allowed=[
        "new",
        "contacted",
        "qualified",
        "proposal",
        "won",
        "lost"
    ]


    if status not in allowed:

        return JsonResponse(
            {
                "success":False
            }
        )


    if request.user.role=="admin":

        lead=get_object_or_404(
            Lead,
            id=lead_id
        )

    else:

        lead=get_object_or_404(
            Lead,
            id=lead_id,
            assigned_to=request.user
        )



    old_status=lead.status


    lead.status=status

    lead.save()



    return JsonResponse(
        {
            "success":True,
            "old_status":old_status,
            "new_status":status
        }
    )



# ==================================================
# CONVERT TO DEAL
# ==================================================

@login_required
def lead_convert(request,pk):

    lead=get_object_or_404(
        Lead,
        pk=pk
    )


    if request.user.role!="admin":

        if lead.assigned_to != request.user:

            messages.error(
                request,
                "Permission denied."
            )

            return redirect(
                "leads:lead_detail",
                pk=pk
            )


    if lead.status!="won":

        messages.warning(
            request,
            "Only won leads can become deals."
        )

        return redirect(
            "leads:lead_detail",
            pk=pk
        )


    if hasattr(lead,"deal"):

        return redirect(
            "deals:deal_detail",
            pk=lead.deal.pk
        )



    if request.method=="POST":

        with transaction.atomic():

            deal=Deal.objects.create(

                lead=lead,

                amount=
                lead.estimated_value,

                stage="negotiation"

            )


        messages.success(
            request,
            "Lead converted into Deal."
        )


        return redirect(
            "deals:deal_detail",
            pk=deal.pk
        )



    return render(
        request,
        "leads/lead_convert.html",
        {
            "lead":lead
        }
    )