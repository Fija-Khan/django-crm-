from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Sum, Avg
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DealForm
from .models import Deal


# ==========================================================
# HELPER FUNCTION
# ==========================================================

def get_user_deals(user):

    if user.role == "admin":

        return Deal.objects.all()

    return Deal.objects.filter(
        lead__assigned_to=user
    )



# ==========================================================
# DEAL LIST
# ==========================================================

@login_required
def deal_list(request):

    deals = (
        get_user_deals(request.user)
        .select_related(
            "lead",
            "lead__contact",
            "lead__assigned_to",
        )
        .order_by("-created_at")
    )


    # ==========================
    # SEARCH
    # ==========================

    search = request.GET.get("search")

    if search:

        deals = deals.filter(
            lead__title__icontains=search
        )



    # ==========================
    # STAGE FILTER
    # ==========================

    stage = request.GET.get("stage")

    if stage:

        deals = deals.filter(
            stage=stage
        )



    # ==========================
    # REVENUE SUMMARY
    # ==========================

    total_deals = deals.count()


    total_revenue = deals.filter(
        stage="closed_won"
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0



    average_deal = deals.aggregate(
        avg=Avg("amount")
    )["avg"] or 0



    # ==========================
    # PAGINATION
    # ==========================

    paginator = Paginator(
        deals,
        10
    )


    page_obj = paginator.get_page(
        request.GET.get("page")
    )



    return render(
        request,
        "deals/deal_list.html",
        {

            "deals": page_obj,

            "page_obj": page_obj,

            "stage_choices": Deal.STAGE_CHOICES,

            "total_deals": total_deals,

            "total_revenue": total_revenue,

            "average_deal": average_deal,

        }
    )



# ==========================================================
# CREATE DEAL
# ==========================================================

@login_required
def deal_create(request):


    if request.method == "POST":


        form = DealForm(
            request.POST
        )


        if form.is_valid():


            deal = form.save(
                commit=False
            )



            # ==========================
            # PERMISSION CHECK
            # ==========================

            if request.user.role != "admin":


                if deal.lead.assigned_to != request.user:


                    messages.error(
                        request,
                        "You cannot create deal for this lead."
                    )


                    return redirect(
                        "deals:deal_list"
                    )



            # ==========================
            # ONLY WON LEAD CONVERT TO DEAL
            # ==========================

            if deal.lead.status != "won":


                messages.warning(
                    request,
                    "Only won leads can be converted into deals."
                )


                return redirect(
                    "deals:deal_list"
                )



            # ==========================
            # DUPLICATE CHECK
            # ==========================

            if Deal.objects.filter(
                lead=deal.lead
            ).exists():


                messages.warning(
                    request,
                    "Deal already exists for this lead."
                )


                return redirect(
                    "deals:deal_list"
                )



            # ==========================
            # SAVE DEAL
            # ==========================

            with transaction.atomic():

                deal.save()



            messages.success(
                request,
                "Deal created successfully."
            )


            return redirect(
                "deals:deal_detail",
                pk=deal.pk
            )



        else:


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
            "form": form
        }
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

        pk=pk
    )



    # Permission

    if request.user.role != "admin":


        if deal.lead.assigned_to != request.user:


            messages.error(
                request,
                "You don't have permission."
            )


            return redirect(
                "deals:deal_list"
            )



    return render(
        request,
        "deals/deal_detail.html",
        {
            "deal": deal
        }
    )



# ==========================================================
# EDIT DEAL
# ==========================================================

@login_required
def deal_edit(request, pk):


    deal = get_object_or_404(
        Deal,
        pk=pk
    )



    # Permission

    if request.user.role != "admin":


        if deal.lead.assigned_to != request.user:


            messages.error(
                request,
                "Permission denied."
            )


            return redirect(
                "deals:deal_list"
            )



    if request.method == "POST":


        form = DealForm(
            request.POST,
            instance=deal
        )



        if form.is_valid():


            selected_lead = form.cleaned_data["lead"]



            # Duplicate lead check

            if Deal.objects.filter(
                lead=selected_lead
            ).exclude(
                pk=deal.pk
            ).exists():


                messages.warning(
                    request,
                    "Another deal already exists for this lead."
                )


                return redirect(
                    "deals:deal_edit",
                    pk=deal.pk
                )



            with transaction.atomic():

                form.save()



            messages.success(
                request,
                "Deal updated successfully."
            )


            return redirect(
                "deals:deal_detail",
                pk=deal.pk
            )



        else:


            messages.error(
                request,
                "Please correct the errors below."
            )



    else:


        form = DealForm(
            instance=deal
        )



    return render(
        request,
        "deals/deal_form.html",
        {
            "form": form,
            "deal": deal,
        }
    )



# ==========================================================
# DELETE DEAL
# ==========================================================

@login_required
def deal_delete(request, pk):


    deal = get_object_or_404(
        Deal,
        pk=pk
    )



    # Permission

    if request.user.role != "admin":


        if deal.lead.assigned_to != request.user:


            messages.error(
                request,
                "Permission denied."
            )


            return redirect(
                "deals:deal_list"
            )



    if request.method == "POST":


        with transaction.atomic():

            deal.delete()



        messages.success(
            request,
            "Deal deleted successfully."
        )


        return redirect(
            "deals:deal_list"
        )



    return render(
        request,
        "deals/deal_confirm_delete.html",
        {
            "deal": deal
        }
    )