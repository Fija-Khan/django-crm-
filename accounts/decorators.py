from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import redirect



# =====================================
# ADMIN REQUIRED DECORATOR
# =====================================

def admin_required(view_func):

    def check_admin(user):

        return (
            user.is_authenticated
            and user.role == "admin"
        )


    def wrapped_view(request, *args, **kwargs):

        if check_admin(request.user):

            return view_func(
                request,
                *args,
                **kwargs
            )


        messages.error(
            request,
            "Admin access required."
        )


        return redirect(
            "dashboard"
        )


    return wrapped_view





# =====================================
# AGENT REQUIRED DECORATOR
# =====================================

def agent_required(view_func):


    def check_agent(user):

        return (
            user.is_authenticated
            and user.role in [
                "admin",
                "agent"
            ]
        )



    def wrapped_view(request, *args, **kwargs):


        if check_agent(request.user):

            return view_func(
                request,
                *args,
                **kwargs
            )


        messages.error(
            request,
            "Agent access required."
        )


        return redirect(
            "dashboard"
        )


    return wrapped_view