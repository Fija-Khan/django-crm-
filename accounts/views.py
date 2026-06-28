from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required


def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ✅ ROLE BASED REDIRECT (IMPORTANT)
            if user.role == "admin":
                return redirect('dashboard')
            else:
                return redirect('dashboard')

        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # New user needs admin approval
            user.is_active = False

            user.save()

            messages.success(
                request,
                "Registration successful. Wait for admin approval."
            )

            return redirect("login")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )
    
    
@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")

        if request.FILES.get("profile_pic"):
            user.profile_pic = request.FILES.get("profile_pic")

        user.save()
        return redirect('profile')

    return render(request, "accounts/profile.html", {"user": user})