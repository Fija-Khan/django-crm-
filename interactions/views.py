from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import InteractionForm
from .models import Interaction


# ==========================================
# INTERACTION LIST
# ==========================================

class InteractionListView(LoginRequiredMixin, ListView):

    model = Interaction

    template_name = "interactions/interaction_list.html"

    context_object_name = "interactions"



    def get_queryset(self):

        queryset = (
            Interaction.objects
            .select_related(
                "contact",
                "lead",
                "logged_by",
            )
            .order_by(
                "-interaction_date"
            )
        )


        # Admin -> All interactions
        # Agent -> Own interactions only

        if self.request.user.role != "admin":

            queryset = queryset.filter(
                logged_by=self.request.user
            )



        # Filter by interaction type

        interaction_type = self.request.GET.get(
            "type"
        )


        if interaction_type:

            queryset = queryset.filter(
                interaction_type=interaction_type
            )


        return queryset





# ==========================================
# CREATE INTERACTION
# ==========================================

class InteractionCreateView(
    LoginRequiredMixin,
    CreateView
):

    model = Interaction

    form_class = InteractionForm

    template_name = "interactions/interaction_form.html"


    success_url = reverse_lazy(
        "interactions:interaction_list"
    )



    def form_valid(self, form):

        # Automatically assign logged user

        form.instance.logged_by = self.request.user


        messages.success(
            self.request,
            "Interaction created successfully."
        )


        return super().form_valid(form)







# ==========================================
# UPDATE INTERACTION
# ==========================================

class InteractionUpdateView(
    LoginRequiredMixin,
    UpdateView
):

    model = Interaction

    form_class = InteractionForm

    template_name = "interactions/interaction_form.html"


    success_url = reverse_lazy(
        "interactions:interaction_list"
    )



    def get_queryset(self):

        queryset = Interaction.objects.select_related(
            "contact",
            "lead",
            "logged_by",
        )


        # Admin -> edit all
        # Agent -> edit own only

        if self.request.user.role != "admin":

            queryset = queryset.filter(
                logged_by=self.request.user
            )


        return queryset




    def form_valid(self, form):

        messages.success(
            self.request,
            "Interaction updated successfully."
        )


        return super().form_valid(form)







# ==========================================
# DELETE INTERACTION
# ==========================================

class InteractionDeleteView(
    LoginRequiredMixin,
    DeleteView
):

    model = Interaction

    template_name = "interactions/interaction_confirm_delete.html"


    success_url = reverse_lazy(
        "interactions:interaction_list"
    )



    def get_queryset(self):

        queryset = Interaction.objects.select_related(
            "contact",
            "lead",
            "logged_by",
        )


        # Admin -> delete all
        # Agent -> delete own only

        if self.request.user.role != "admin":

            queryset = queryset.filter(
                logged_by=self.request.user
            )


        return queryset




    def form_valid(self, form):

        messages.success(
            self.request,
            "Interaction deleted successfully."
        )


        return super().form_valid(form)