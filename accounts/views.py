from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

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
@never_cache
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
@never_cache
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect("login")


# ---------------- PROFILE ----------------
@never_cache
@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # 📸 1️⃣ UPLOAD ΦΩΤΟΓΡΑΦΙΑΣ
    if request.method == "POST" and request.FILES.get("profile_image"):
        profile.profile_image = request.FILES.get("profile_image")
        profile.save()
        messages.success(request, "Η εικόνα προφίλ ενημερώθηκε!")
        return redirect("profile")

    # ✏️ 2️⃣ INLINE EDIT (username, email, Birth_Date)
    if request.method == "POST" and not request.FILES:
        user = request.user

        username = request.POST.get("username")
        email = request.POST.get("email")
        birth_date = request.POST.get("birth_date")

        if username:
            user.username = username
        if email:
            user.email = email
        if birth_date:
            profile.Birth_Date = birth_date

        user.save()
        profile.save()

        messages.success(request, "Το προφίλ ενημερώθηκε!")
        return redirect("profile")

    # GET
    form = ProfileForm(instance=profile)

    return render(request, "accounts/profile.html", {
        "profile": profile,
        "form": form
    })


# ---------------- FORGOT PASSWORD ----------------
def forgot_password(request):
    return render(request, "accounts/forgot_password.html")
