from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import DealForm
from .models import Deal


# ==========================================================
# DEAL LIST
# ==========================================================

@login_required
def deal_list(request):

    deals = (
        Deal.objects
        .select_related(
            "lead",
            "lead__contact",
            "lead__assigned_to",
        )
        .order_by("-id")
    )

    return render(
        request,
        "deals/deal_list.html",
        {
            "deals": deals,
        },
    )


# ==========================================================
# CREATE DEAL
# ==========================================================

@login_required
def deal_create(request):

    if request.method == "POST":

        form = DealForm(request.POST)

        if form.is_valid():

            deal = form.save()

            messages.success(
                request,
                "Deal created successfully."
            )

            return redirect(
                "deals:deal_detail",
                pk=deal.pk,
            )

        messages.error(
            request,
            "Please correct the errors below."
        )

    else:

        form = DealForm()

    return render(
        request,
        "deals/deal_form.html",
        {
            "form": form,
        },
    )


# ==========================================================
# DEAL DETAIL
# ==========================================================

@login_required
def deal_detail(request, pk):

    deal = get_object_or_404(
        Deal.objects.select_related(
            "lead",
            "lead__contact",
            "lead__assigned_to",
        ),
        pk=pk,
    )

    return render(
        request,
        "deals/deal_detail.html",
        {
            "deal": deal,
        },
    )


# ==========================================================
# EDIT DEAL
# ==========================================================

@login_required
def deal_edit(request, pk):

    deal = get_object_or_404(
        Deal,
        pk=pk,
    )

    if request.method == "POST":

        form = DealForm(
            request.POST,
            instance=deal,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Deal updated successfully."
            )

            return redirect(
                "deals:deal_detail",
                pk=deal.pk,
            )

        messages.error(
            request,
            "Please correct the errors below."
        )

    else:

        form = DealForm(
            instance=deal,
        )

    return render(
        request,
        "deals/deal_form.html",
        {
            "form": form,
            "deal": deal,
        },
    )


# ==========================================================
# DELETE DEAL
# ==========================================================

@login_required
def deal_delete(request, pk):

    deal = get_object_or_404(
        Deal,
        pk=pk,
    )

    if request.method == "POST":

        deal.delete()

        messages.success(
            request,
            "Deal deleted successfully."
        )

        return redirect(
            "deals:deal_list",
        )

    return render(
        request,
        "deals/deal_confirm_delete.html",
        {
            "deal": deal,
        },
    )