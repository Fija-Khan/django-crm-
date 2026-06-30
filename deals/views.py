from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Deal
from .forms import DealForm


# 📋 DEAL LIST
@login_required
def deal_list(request):
    deals = Deal.objects.select_related('lead').all()
    return render(request, "deals/deal_list.html", {"deals": deals})


# ➕ DEAL CREATE
@login_required
def deal_create(request):
    if request.method == "POST":
        form = DealForm(request.POST)
        if form.is_valid():
            deal = form.save()
            return redirect("deal_detail", pk=deal.pk)
    else:
        form = DealForm()

    return render(request, "deals/deal_form.html", {"form": form})


# 👁️ DEAL DETAIL
@login_required
def deal_detail(request, pk):
    deal = get_object_or_404(Deal, pk=pk)
    return render(request, "deals/deal_detail.html", {"deal": deal})


# ✏️ DEAL EDIT
@login_required
def deal_edit(request, pk):
    deal = get_object_or_404(Deal, pk=pk)

    if request.method == "POST":
        form = DealForm(request.POST, instance=deal)
        if form.is_valid():
            form.save()
            return redirect("deal_detail", pk=deal.pk)
    else:
        form = DealForm(instance=deal)

    return render(request, "deals/deal_form.html", {"form": form, "deal": deal})


# ❌ DEAL DELETE
@login_required
def deal_delete(request, pk):
    deal = get_object_or_404(Deal, pk=pk)

    if request.method == "POST":
        deal.delete()
        return redirect("deal_list")

    return render(request, "deals/deal_confirm_delete.html", {"deal": deal})