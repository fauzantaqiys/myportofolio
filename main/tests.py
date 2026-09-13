from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Interest


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )
        self.interest = Interest.objects.create(
            title="Pergi ke taman",
            description="Membuat kenangan indah di ruangan hijau terbuka.",
            category="activity",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')
        self.assertNotContains(response, self.interest.title)
        self.assertContains(response, f'href="{reverse("main:show_interest")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

    def test_interest_model(self):
        self.assertEqual(str(self.interest), "Pergi ke taman")
        self.assertEqual(self.interest.category, "activity")

    def test_interest_page(self):
        response = self.client.get(reverse("main:show_interest"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "interest.html")
        self.assertContains(response, self.interest.title)
        self.assertContains(response, self.interest.description)
        self.assertContains(response, "Activity")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_interest_page(self):
        Interest.objects.all().delete()
        response = self.client.get(reverse("main:show_interest"))

        self.assertContains(response, "Belum ada kesenangan yang ditambahkan.")