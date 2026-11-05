from django.urls import path
from main import api_views

app_name = "api"

urlpatterns = [
    # Experience endpoints (Tutorial 7)
    path("experiences/", api_views.experience_list, name="experience-list"),
    path(
        "experiences/<uuid:id>/",
        api_views.experience_detail,
        name="experience-detail",
    ),
    path(
        "experiences/<uuid:id>/star/",
        api_views.experience_star,
        name="experience-star",
    ),
    # Interest endpoints (Tugas 6)
    path("interests/", api_views.interest_list, name="interest-list"),
    path(
        "interests/<uuid:id>/",
        api_views.interest_detail,
        name="interest-detail",
    ),
    path(
        "interests/<uuid:id>/star/",
        api_views.interest_star,
        name="interest-star",
    ),
]
