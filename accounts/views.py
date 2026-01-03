from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import SignupForm, ProfileForm
from .models import UserProfile


# ---------------- SIGN UP ----------------
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            pw = form.cleaned_data["password"]
            user.set_password(pw)
            user.save()

            UserProfile.objects.create(
                user=user,
                Birth_Date=form.cleaned_data.get("Birth_Date")
            )

            messages.success(request, "Ο λογαριασμός δημιουργήθηκε!")
            return redirect("login")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


# ---------------- LOGIN ----------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Λάθος στοιχεία.")
            return redirect("login")

    return render(request, "accounts/login.html")


# ---------------- LOGOUT ----------------
def logout_view(request):
    logout(request)
    return redirect("login")


# ---------------- PROFILE ----------------
@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)


    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Το προφίλ ενημερώθηκε!")
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "accounts/profile.html", {
        "profile": profile,
        "form": form
    })


# ---------------- FORGOT PASSWORD ----------------
def forgot_password(request):
    return render(request, "accounts/forgot_password.html")

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, "accounts/profile.html", {"profile": profile})

