from django.contrib import admin
from .models import SpaceAgency, Mission, Satellite, FavoriteMission


class MissionAdmin(admin.ModelAdmin):
    list_display = ("name", "agency", "status", "orbit_type", "launch_date")
    list_filter = ("status", "orbit_type", "agency")
    search_fields = ("name",)


class SatelliteAdmin(admin.ModelAdmin):
    list_display = ("name", "mission", "orbit_type", "purpose")
    list_filter = ("orbit_type",)


admin.site.register(SpaceAgency)
admin.site.register(Mission, MissionAdmin)
admin.site.register(Satellite, SatelliteAdmin)
admin.site.register(FavoriteMission)


