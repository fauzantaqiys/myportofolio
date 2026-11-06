import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience, Interest


class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com"
        )
        self.visitor = User.objects.create_user(
            username="visitor", password="test-password"
        )
        self.experience = Experience.objects.create(
            title="Portfolio Developer",
            description="Working on personal web app.",
            category="full-time",
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse(
            "api:experience-detail", args=[self.experience.id]
        )
        self.star_url = reverse(
            "api:experience-star", args=[self.experience.id]
        )
        self.payload = {
            "title": "Backend Intern",
            "description": "Building APIs with Django REST Framework.",
            "category": "internship",
            "thumbnail": "https://example.com/photo.png",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.experience.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(
            self.client.get(self.detail_url).status_code, status.HTTP_200_OK
        )

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_experience(self):
        url = reverse("api:experience-detail", args=[uuid.uuid4()])
        self.assertEqual(
            self.client.get(url).status_code, status.HTTP_404_NOT_FOUND
        )

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(
                self.client.post(self.list_url, self.payload, format="json").status_code,
                403,
            )
            self.assertEqual(
                self.client.patch(
                    self.detail_url, {"title": "Changed"}, format="json"
                ).status_code,
                403,
            )
            self.assertEqual(
                self.client.delete(self.detail_url).status_code, 403
            )
        self.assertEqual(Experience.objects.count(), 1)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Portfolio Developer")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Experience.objects.filter(pk=response.data["id"]).exists()
        )

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"category": "invalid-choice"}, "category"),
        ]:
            response = self.client.post(
                self.list_url, {**self.payload, **changes}, format="json"
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Experience.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(
            self.detail_url, {"title": "Changed"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Changed")
        self.assertEqual(
            self.experience.description, "Working on personal web app."
        )

        response = self.client.put(
            self.detail_url, {"title": "Incomplete"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(
            self.detail_url, self.payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(
            Experience.objects.filter(pk=self.experience.id).exists()
        )

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(
            self.client.post(self.star_url).status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)

        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            self.list_url,
            {
                **self.payload,
                "star_count": 99,
                "is_starred": True,
                "starred_by_names": "forged",
                "starred_by": [self.visitor.id],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_tutorial_experience(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(
            self.detail_url, {"title": "Changed"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(
            self.client.delete(self.list_url).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(
            client.login(username="owner", password="test-password")
        )
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url,
            self.payload,
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class InterestAPITest(APITestCase):
    """
    Test suite komprehensif untuk Tugas 6 (Interest DRF API).
    Mencakup hak akses ke-4 peran (Anonim, Pengguna biasa, Editor, Superuser),
    validasi input, perlindungan CSRF, dan integritas database.
    """

    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com"
        )
        self.visitor = User.objects.create_user(
            username="visitor", password="test-password"
        )
        self.editor_group = Group.objects.create(name="Editor")
        self.editor = User.objects.create_user(
            username="editor", password="test-password"
        )
        self.editor.groups.add(self.editor_group)

        self.interest = Interest.objects.create(
            title="Listening to Jazz",
            description="Enjoying classic jazz albums.",
            category="music",
        )
        self.list_url = reverse("api:interest-list")
        self.detail_url = reverse(
            "api:interest-detail", args=[self.interest.id]
        )
        self.star_url = reverse(
            "api:interest-star", args=[self.interest.id]
        )
        self.payload = {
            "title": "Street Photography",
            "description": "Capturing city life on film.",
            "category": "activity",
            "thumbnail": "https://example.com/photo.jpg",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.interest.id))
        self.assertEqual(response.data[0]["title"], "Listening to Jazz")
        self.assertEqual(response.data[0]["category_display"], "Music")
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])

        detail_response = self.client.get(self.detail_url)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data["title"], "Listening to Jazz")

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "Jazz"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "non-existent-interest"})
        self.assertEqual(response.data, [])

    def test_missing_interest(self):
        url = reverse("api:interest-detail", args=[uuid.uuid4()])
        self.assertEqual(
            self.client.get(url).status_code, status.HTTP_404_NOT_FOUND
        )

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(
                self.client.post(self.list_url, self.payload, format="json").status_code,
                status.HTTP_403_FORBIDDEN,
            )
            self.assertEqual(
                self.client.patch(
                    self.detail_url, {"title": "Hacked"}, format="json"
                ).status_code,
                status.HTTP_403_FORBIDDEN,
            )
            self.assertEqual(
                self.client.delete(self.detail_url).status_code,
                status.HTTP_403_FORBIDDEN,
            )

        # Verifikasi isi database tidak berubah
        self.assertEqual(Interest.objects.count(), 1)
        self.interest.refresh_from_db()
        self.assertEqual(self.interest.title, "Listening to Jazz")

    def test_editor_can_patch_and_put_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)

        # 1. Editor DITOLAK saat membuat data (POST)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Interest.objects.count(), 1)

        # 2. Editor BERHASIL melakukan PATCH
        response = self.client.patch(
            self.detail_url, {"title": "Cool Jazz"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.interest.refresh_from_db()
        self.assertEqual(self.interest.title, "Cool Jazz")
        self.assertEqual(self.interest.description, "Enjoying classic jazz albums.")

        # 3. Editor BERHASIL melakukan PUT lengkap
        put_payload = {
            "title": "Modern Jazz",
            "description": "Fusion and modern jazz.",
            "category": "music",
            "thumbnail": "https://example.com/jazz.jpg",
        }
        response = self.client.put(self.detail_url, put_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.interest.refresh_from_db()
        self.assertEqual(self.interest.title, "Modern Jazz")

        # 4. Editor DITOLAK saat menghapus data (DELETE)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Interest.objects.filter(pk=self.interest.id).exists())

    def test_owner_can_crud(self):
        self.client.force_authenticate(user=self.owner)

        # CREATE
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_id = response.data["id"]
        self.assertTrue(Interest.objects.filter(pk=new_id).exists())

        # UPDATE (PATCH)
        detail_url = reverse("api:interest-detail", args=[new_id])
        response = self.client.patch(
            detail_url, {"title": "Landscape Photography"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # DELETE
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Interest.objects.filter(pk=new_id).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"category": "invalid-choice"}, "category"),
        ]:
            response = self.client.post(
                self.list_url, {**self.payload, **changes}, format="json"
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)

        # Database tidak bertambah
        self.assertEqual(Interest.objects.count(), 1)

    def test_star_requires_login_and_toggles(self):
        # Anonymous ditolak
        self.assertEqual(
            self.client.post(self.star_url).status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Visitor bisa memberi dan membatalkan star
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)

        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

        # Editor juga bisa memberi star
        self.client.force_authenticate(user=self.editor)
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            self.list_url,
            {
                **self.payload,
                "star_count": 999,
                "is_starred": True,
                "starred_by_names": "forged_user",
                "starred_by": [self.visitor.id],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(
            self.client.delete(self.list_url).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(
            client.login(username="owner", password="test-password")
        )
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Interest.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url,
            self.payload,
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
