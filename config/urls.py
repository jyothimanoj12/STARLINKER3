from django.contrib import admin
from django.urls import path
from starlinker import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # HOME (landing page)
    path("", views.home, name="home"),

    # MISSIONS
    path("missions/", views.missions, name="missions"),

    # MISSION DETAIL
    path("mission/<int:mission_id>/", views.mission_detail, name="mission_detail"),

    # OTHER PAGES
    path("agencies/", views.agencies_list, name="agencies_list"),
    path("iss/", views.iss_tracker, name="iss_tracker"),
    path("astronauts/", views.astronauts, name="astronauts"),
    path("satellites/", views.satellites_live, name="satellites_live"),
    path("ask-ai/", views.ask_ai, name="ask_ai"),

    # AUTH
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # USER
    path("profile/", views.profile_view, name="profile"),
    path("my-missions/", views.my_missions, name="my_missions"),
]










