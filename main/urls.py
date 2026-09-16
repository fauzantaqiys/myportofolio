from django.urls import path
from main.views import show_main, show_experience, show_interest, create_interest, show_json, show_xml, delete_interest

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("interest/", show_interest, name="show_interest"),
    path("interest/add/", create_interest, name="create_interest"),
    path("api/interest/json/", show_json, name="show_json"),
    path("api/interest/xml/", show_xml, name="show_xml"),
    path("interest/<uuid:interest_id>/delete/", delete_interest, name="delete_interest"),
]