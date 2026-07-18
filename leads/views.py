from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import LeadForm
from .models import Lead
from deals.models import Deal


# ==========================================
# LEAD LIST
# ==========================================

@login_required
def lead_list(request):

    leads = (
        Lead.objects
        .select_related("contact", "assigned_to")
        .all()
        .order_by("-created_at")
    )

    return render(
        request,
        "leads/lead_list.html",
        {"leads": leads},
    )


# ==========================================
# ADD LEAD
# ==========================================

@login_required
def lead_add(request):

    if request.method == "POST":

        form = LeadForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Lead created successfully."
            )

            return redirect("leads:lead_list")

        messages.error(
            request,
            "Please correct the errors below."
        )

    else:

        form = LeadForm()

    return render(
        request,
        "leads/lead_form.html",
        {"form": form},
    )


# ==========================================
# LEAD DETAIL
# ==========================================

@login_required
def lead_detail(request, pk):

    lead = get_object_or_404(
        Lead.objects.select_related(
            "contact",
            "assigned_to",
        ),
        pk=pk,
    )

    return render(
        request,
        "leads/lead_detail.html",
        {"lead": lead},
    )


# ==========================================
# EDIT LEAD
# ==========================================

@login_required
def lead_edit(request, pk):

    lead = get_object_or_404(Lead, pk=pk)

    if request.method == "POST":

        form = LeadForm(request.POST, instance=lead)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Lead updated successfully."
            )

            return redirect(
                "leads:lead_detail",
                pk=lead.pk,
            )

        messages.error(
            request,
            "Please correct the errors below."
        )

    else:

        form = LeadForm(instance=lead)

    return render(
        request,
        "leads/lead_form.html",
        {
            "form": form,
            "lead": lead,
        },
    )


# ==========================================
# DELETE LEAD
# ==========================================

@login_required
def lead_delete(request, pk):

    lead = get_object_or_404(
        Lead,
        pk=pk,
    )

    if request.method == "POST":

        lead.delete()

        messages.success(
            request,
            "Lead deleted successfully."
        )

        return redirect("leads:lead_list")

    return render(
        request,
        "leads/lead_confirm_delete.html",
        {
            "lead": lead,
        },
    )


# ==========================================
# LEAD KANBAN BOARD
# ==========================================

@login_required
def lead_kanban(request):

    context = {

        "new_leads": Lead.objects.filter(status="new"),

        "contacted_leads": Lead.objects.filter(status="contacted"),

        "qualified_leads": Lead.objects.filter(status="qualified"),

        "proposal_leads": Lead.objects.filter(status="proposal"),

        "won_leads": Lead.objects.filter(status="won"),

        "lost_leads": Lead.objects.filter(status="lost"),
    }

    return render(
        request,
        "leads/lead_kanban.html",
        context,
    )


# ==========================================
# UPDATE LEAD STATUS (AJAX)
# ==========================================

@require_POST
@login_required
def update_stage(request):

    lead_id = request.POST.get("lead_id")
    status = request.POST.get("status")

    valid_status = [
        "new",
        "contacted",
        "qualified",
        "proposal",
        "won",
        "lost",
    ]

    if not lead_id or not status:

        return JsonResponse({
            "success": False,
            "message": "Missing required data.",
        })

    if status not in valid_status:

        return JsonResponse({
            "success": False,
            "message": "Invalid status.",
        })

    try:

        lead = Lead.objects.get(id=lead_id)

        lead.status = status
        lead.save()

        return JsonResponse({
            "success": True,
            "message": "Lead status updated successfully.",
        })

    except Lead.DoesNotExist:

        return JsonResponse({
            "success": False,
            "message": "Lead not found.",
        })


# ==========================================
# CONVERT LEAD TO DEAL
# ==========================================

@login_required
def lead_convert(request, pk):

    lead = get_object_or_404(Lead, pk=pk)

    # Prevent duplicate conversion
    if hasattr(lead, "deal"):

        messages.warning(
            request,
            "This lead has already been converted."
        )

        return redirect(
            "deals:deal_detail",
            pk=lead.deal.pk,
        )

    if request.method == "POST":

        deal = Deal.objects.create(
            lead=lead,
            amount=0,
            stage="negotiation",
        )

        messages.success(
            request,
            "Lead converted into Deal successfully."
        )

        return redirect(
            "deals:deal_detail",
            pk=deal.pk,
        )

    return render(
        request,
        "leads/lead_convert.html",
        {
            "lead": lead,
        },
    )