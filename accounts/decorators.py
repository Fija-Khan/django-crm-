from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps



# =====================================
# ADMIN REQUIRED DECORATOR
# =====================================

def admin_required(view_func):


    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):


        if (
            request.user.is_authenticated
            and request.user.role == "admin"
        ):

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


    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):


        if (
            request.user.is_authenticated
            and request.user.role == "agent"
        ):

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