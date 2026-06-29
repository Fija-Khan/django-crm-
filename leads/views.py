from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .models import Lead
from .forms import LeadForm


# -------------------------
# LEAD LIST
# -------------------------
@login_required
def lead_list(request):
    leads = Lead.objects.all().order_by("-created_at")

    return render(request, "leads/lead_list.html", {
        "leads": leads
    })


# -------------------------
# ADD LEAD
# -------------------------
@login_required
def lead_add(request):

    if request.method == "POST":
        form = LeadForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("lead_list")

    else:
        form = LeadForm()

    return render(request, "leads/lead_form.html", {
        "form": form
    })


# -------------------------
# LEAD DETAIL
# -------------------------
@login_required
def lead_detail(request, pk):

    lead = get_object_or_404(Lead, pk=pk)

    return render(request, "leads/lead_detail.html", {
        "lead": lead
    })


# -------------------------
# EDIT LEAD
# -------------------------
@login_required
def lead_edit(request, pk):

    lead = get_object_or_404(Lead, pk=pk)

    if request.method == "POST":
        form = LeadForm(request.POST, instance=lead)

        if form.is_valid():
            form.save()
            return redirect("lead_detail", pk=lead.pk)

    else:
        form = LeadForm(instance=lead)

    return render(request, "leads/lead_form.html", {
        "form": form,
        "lead": lead
    })


# -------------------------
# DELETE LEAD
# -------------------------
@login_required
def lead_delete(request, pk):

    lead = get_object_or_404(Lead, pk=pk)

    if request.method == "POST":
        lead.delete()
        return redirect("lead_list")

    return render(request, "leads/lead_confirm_delete.html", {
        "lead": lead
    })


# -------------------------
# KANBAN BOARD
# -------------------------
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

    return render(request, "leads/lead_kanban.html", context)


# -------------------------
# UPDATE STAGE (AJAX)
# -------------------------
@require_POST
@login_required
def update_stage(request):

    lead_id = request.POST.get("lead_id")
    status = request.POST.get("status")

    if not lead_id or not status:
        return JsonResponse({
            "success": False,
            "message": "Missing data"
        })

    try:
        lead = Lead.objects.get(id=lead_id)
        lead.status = status
        lead.save()

        return JsonResponse({
            "success": True,
            "message": "Lead updated successfully"
        })

    except Lead.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Lead not found"
        })