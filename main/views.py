from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.core import serializers
from main.models import Experience, Interest
from main.forms import InterestForm

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

def show_interest(request):
    # 1. Panggil fungsi API JSON yang sudah difilter
    json_response = show_json(request)
    
    # 2. Deserialize (Ubah) format JSON kembali ke bentuk objek Python
    interests = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    
    # 3. Ekstrak isi objek aslinya dari hasil deserialisasi
    interests = [interest.object for interest in interests]
    
    # 4. Ambil query pencarian untuk dikembalikan ke template
    title_query = request.GET.get("title", "").strip()
    
    context = {
        "name": "Fauzan Taqiy Santosa",
        "interest_list": interests,
        "title_query": title_query,
    }
    return render(request, "interest.html", context)

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

def show_json(request):
    # Mengambil query pencarian 'title' dari URL
    title_query = request.GET.get("title", "").strip()
    
    # Melakukan filter data jika ada kata kunci yang dicari
    if title_query:
        data = Interest.objects.filter(title__icontains=title_query)
    else:
        data = Interest.objects.all()
        
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml(request):
    # Mengambil semua data dari model Interest
    data = Interest.objects.all()
    
    # Mengubah data menjadi format XML dan mengembalikannya
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def delete_interest(request, interest_id):
    interest = get_object_or_404(Interest, pk=interest_id)

    if request.method == "POST":
        interest.delete()
        messages.success(request, "Kesenangan berhasil dihapus!")
        return redirect("main:show_interest")

    return redirect("main:show_interest")