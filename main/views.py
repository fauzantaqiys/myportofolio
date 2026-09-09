from django.shortcuts import render
from main.models import Experience

def show_main(request):
    context = {
        "name": "Fauzan Taqiy Santosa",
        "npm": "2506607272",
        "study_program": "S1 Sistem Informasi",
        "bio": "Halo semuanya! Saya Fauzan Taqiy Santosa, seorang mahasiswa Sistem Informasi di Universitas Indonesia.",
    }
    return render(request, "index.html", context)

def show_experience(request):
    context = {
        "name": "Fauzan Taqiy Santosa",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)