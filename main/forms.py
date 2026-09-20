from django.forms import ModelForm, TextInput, Textarea, URLInput, DateTimeInput

from main.models import Interest, Experience

class InterestForm(ModelForm):
    class Meta:
        model = Interest
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
        ]

        labels = {
            "title": "Nama Kesenangan",
            "description": "Deskripsi Kesenangan",
            "category": "Jenis Kesenangan",
            "thumbnail": "Gambar Kesenangan"
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Hiking, PLaying guitar, etc.",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Kesenanganmu",
                    "rows": 3,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at"
        ]

        labels = {
            "title": "Nama Pengalaman",
            "description": "Deskripsi Pengalaman",
            "category": "Jenis Pengalaman",
            "thumbnail": "Gambar Pengalaman",
            "started_at": "Waktu dimulai",
            "ended_at": "Waktu berakhir"
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Organisasi, Kepanitaan, etc.",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Pengalamanmu",
                    "rows": 3,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
            "started_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
            "ended_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
        }