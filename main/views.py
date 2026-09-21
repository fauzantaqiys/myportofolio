from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied        
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse
from django.core import serializers
from main.models import Experience, Interest
from main.forms import InterestForm, ExperienceForm

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Fauzan Taqiy Santosa",
        "npm": "2506607272",
        "study_program": "S1 Sistem Informasi",
        "bio": "Halo semuanya! Saya Fauzan Taqiy Santosa, seorang mahasiswa Sistem Informasi di Universitas Indonesia.",
         "last_login": last_login,
    }
    return render(request, "index.html", context)

def show_experience(request):
    # 1. Panggil fungsi API JSON yang sudah difilter
    json_response = show_json_experience(request)
    
    # 2. Deserialize (Ubah) format JSON kembali ke bentuk objek Python
    deserialized_data = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    
    # 3. Ekstrak isi objek aslinya dari hasil deserialisasi
    experiences = [experience.object for experience in deserialized_data]
    
    # 4. Ambil query pencarian untuk dikembalikan ke template
    title_query = request.GET.get("title", "").strip()
    
    context = {
        "name": "Fauzan Taqiy Santosa",
        "experience_list": experiences,
        "title_query": title_query,
    }
    return render(request, "experience.html", context)

def show_interest(request):
    # 1. Panggil fungsi API JSON yang sudah difilter
    json_response = show_json_interest(request)
    
    # 2. Deserialize (Ubah) format JSON kembali ke bentuk objek Python
    deserialized_data = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    
    # 3. Ekstrak isi objek aslinya dari hasil deserialisasi
    interests = [interest.object for interest in deserialized_data]
    
    # 4. Ambil query pencarian untuk dikembalikan ke template
    title_query = request.GET.get("title", "").strip()
    
    context = {
        "name": "Fauzan Taqiy Santosa",
        "interest_list": interests,
        "title_query": title_query,
    }
    return render(request, "interest.html", context)

@login_required(login_url="/login/")
def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Fauzan Taqiy Santosa",
        "form": form,
    }
    return render(request, "experience_form.html", context)

@login_required(login_url="/login/")
def create_interest(request):
    form = InterestForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Kesenangan baru berhasil ditambahkan!")
        return redirect("main:show_interest")

    context = {
        "name": "Fauzan Taqiy Santosa",
        "form": form,
    }
    return render(request, "interest_form.html", context)

def show_json_interest(request):
    title_query = request.GET.get("title", "").strip()
    
    if title_query:
        data = Interest.objects.filter(title__icontains=title_query)
    else:
        data = Interest.objects.all()
        
    return HttpResponse(
        serializers.serialize(
            "json",
            data,
            use_natural_foreign_keys=True
        ),
        content_type="application/json"
    )

def show_json_experience(request):
    title_query = request.GET.get("title", "").strip()
    
    if title_query:
        data = Experience.objects.filter(title__icontains=title_query)
    else:
        data = Experience.objects.all()
        
    return HttpResponse(
        serializers.serialize(
            "json",
            data,
            use_natural_foreign_keys=True
        ),
        content_type="application/json"
    )

def show_xml_interest(request):
    # Mengambil semua data dari model Interest
    data = Interest.objects.all()
    
    # Mengubah data menjadi format XML dan mengembalikannya
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_xml_experience(request):
    # Mengambil semua data dari model Interest
    data = Experience.objects.all()
    
    # Mengubah data menjadi format XML dan mengembalikannya
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@login_required(login_url="/login/")
def delete_interest(request, interest_id):
    interest = get_object_or_404(Interest, pk=interest_id)

    if request.method == "POST":
        interest.delete()
        messages.success(request, "Kesenangan berhasil dihapus!")
        return redirect("main:show_interest")

    return redirect("main:show_interest")

@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

@login_required(login_url="/login/")
def edit_experience(request, id):
    # Ambil data spesifik berdasarkan ID
    experience = get_object_or_404(Experience, pk=id)
    
    # Masukkan data lama ke dalam form menggunakan argumen 'instance'
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Fauzan Taqiy Santosa",
        "form": form,
    }
    # Kita bisa menggunakan template form yang sama dengan form create
    return render(request, "experience_form.html", context)

@login_required(login_url="/login/")
def edit_interest(request, id):
    interest = get_object_or_404(Interest, pk=id)
    form = InterestForm(request.POST or None, instance=interest)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Kesenangan berhasil diperbarui!")
        return redirect("main:show_interest")

    context = {
        "name": "Fauzan Taqiy Santosa",
        "form": form,
    }
    return render(request, "interest_form.html", context)

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Fauzan Taqiy Santosa",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Fauzan Taqiy Santosa",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
def toggle_star_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")

@login_required(login_url="/login/")
def toggle_star_interest(request, interest_id):
    interest = get_object_or_404(Interest, pk=interest_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in interest.starred_by.all():
            interest.starred_by.remove(request.user)
        else:
            interest.starred_by.add(request.user)

    return redirect("main:show_interest")