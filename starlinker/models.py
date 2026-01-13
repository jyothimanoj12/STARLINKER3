from django.db import models
from django.contrib.auth.models import User


class SpaceAgency(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    founded = models.IntegerField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    logo = models.ImageField(upload_to="agency_logos/", null=True, blank=True)

    def __str__(self):
        return self.name


class Mission(models.Model):
    ORBIT_TYPES = [
        ("LEO", "Low Earth Orbit"),
        ("MEO", "Medium Earth Orbit"),
        ("GEO", "Geostationary Orbit"),
        ("HEO", "High Earth Orbit"),
        ("OTHER", "Other"),
    ]

    agency = models.ForeignKey(SpaceAgency, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    launch_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50)  # Upcoming / Completed / Failed etc.
    orbit_type = models.CharField(
        max_length=20, choices=ORBIT_TYPES, default="OTHER"
    )
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="mission_images/", null=True, blank=True)

    def launch_year(self):
        return self.launch_date.year if self.launch_date else None

    def __str__(self):
        return self.name


class Satellite(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    orbit_type = models.CharField(max_length=50, blank=True)
    purpose = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class FavoriteMission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mission = models.ForeignKey(
        Mission,
        on_delete=models.CASCADE,
        related_name="favorites"
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "mission")

    def __str__(self):
        return f"{self.user.username} → {self.mission.name}"




