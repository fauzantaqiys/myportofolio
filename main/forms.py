from django.forms import ModelForm, TextInput, Textarea, URLInput

from main.models import Interest

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
                    "placeholder": "Portfolio Website",
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