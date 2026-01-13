from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Mission, SpaceAgency, FavoriteMission
from .forms import SignUpForm

import wikipedia
wikipedia.set_lang("en")


# ================= HOME =================
def home(request):
    return render(request, "starlinker/home.html")


# ================= MISSIONS =================
def missions(request):
    missions = Mission.objects.all()

    status = request.GET.get("status")
    agency = request.GET.get("agency")
    year = request.GET.get("year")
    orbit = request.GET.get("orbit")
    search = request.GET.get("search")

    if search:
        missions = missions.filter(name__icontains=search)

    if status:
        missions = missions.filter(status__iexact=status)

    if agency:
        missions = missions.filter(agency__id=agency)

    if year:
        missions = missions.filter(launch_date__year=year)

    if orbit:
        missions = missions.filter(orbit_type=orbit)

    years = (
        Mission.objects.exclude(launch_date=None)
        .values_list("launch_date__year", flat=True)
        .distinct()
        .order_by("-launch_date__year")
    )

    return render(
        request,
        "starlinker/missions.html",
        {
            "missions": missions,
            "agencies": SpaceAgency.objects.all(),
            "years": years,
            "selected_status": status,
            "selected_agency": agency,
            "selected_year": year,
            "selected_orbit": orbit,
            "search": search,
        }
    )


def mission_detail(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)
    return render(request, "starlinker/mission_detail.html", {"mission": mission})


# ================= OTHER PAGES =================
def agencies_list(request):
    agencies = SpaceAgency.objects.all()
    return render(
        request,
        "starlinker/agencies_list.html",
        {"agencies": agencies}
    )



def iss_tracker(request):
    return render(request, "starlinker/iss_tracker.html")


def astronauts(request):
    return render(request, "starlinker/astronauts.html")


def satellites_live(request):
    return render(request, "starlinker/satellites_live.html")


def ask_ai(request):
    answer = None
    if request.method == "POST":
        question = request.POST.get("question")
        try:
            answer = wikipedia.summary(question, sentences=2)
        except:
            answer = "No result found."
    return render(request, "starlinker/ask_ai.html", {"answer": answer})


# ================= AUTH =================
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "starlinker/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )
        if user:
            login(request, user)
            return redirect("home")
        messages.error(request, "Invalid credentials")
    return render(request, "starlinker/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


# ================= USER =================
@login_required
def profile_view(request):
    return render(request, "starlinker/profile.html")


@login_required
def my_missions(request):
    missions = Mission.objects.filter(favorites__user=request.user)
    return render(request, "starlinker/my_missions.html", {"missions": missions})


