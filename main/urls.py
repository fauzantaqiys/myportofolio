from django.urls import path
# 1. PERBAIKAN: Import nama-nama fungsi baru dari views.py
from main.views import (
    show_main, 
    show_experience, 
    show_interest, 
    create_interest, 
    create_experience, 
    show_json_interest, 
    show_json_experience, 
    show_xml_interest, 
    show_xml_experience, 
    delete_interest, 
    delete_experience,
    edit_experience,
    edit_interest,
    register,
    login_user,
    logout_user,
    toggle_star_experience,
    toggle_star_interest
)

app_name = "main"

urlpatterns = [
    # Halaman Utama & Form
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("interest/", show_interest, name="show_interest"),
    path("interest/add/", create_interest, name="create_interest"),
    path("experience/add/", create_experience, name="create_experience"),
    
    # Endpoint API JSON & XML untuk Interest
    path("api/interest/json/", show_json_interest, name="show_json_interest"),
    path("api/interest/xml/", show_xml_interest, name="show_xml_interest"),
    
    # Tambahkan Endpoint API JSON & XML untuk Experience
    path("api/experience/json/", show_json_experience, name="show_json_experience"),
    path("api/experience/xml/", show_xml_experience, name="show_xml_experience"),
    
    # Tombol Aksi Hapus (Delete)
    path("interest/<uuid:interest_id>/delete/", delete_interest, name="delete_interest"),
    # Diubah target fungsinya ke delete_experience dan parameternya menjadi experience_id
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),

    path("experience/<uuid:id>/edit/", edit_experience, name="edit_experience"),
    path("interest/<uuid:id>/edit/", edit_interest, name="edit_interest"),

    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),

    path("experiences/<uuid:experience_id>/star/", toggle_star_experience, name="toggle_star_experience"),
    path("interests/<uuid:interest_id>/star/", toggle_star_interest, name="toggle_star_interest"),
]
