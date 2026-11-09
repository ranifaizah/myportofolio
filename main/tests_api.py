
import uuid

from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience


class ExperienceAPITest(APITestCase):
    """
    Automated tests for Experience REST API.

    Roles:
    1. Anonymous visitor
    2. Regular user
    3. Editor
    4. Portfolio owner (superuser)
    """

    def setUp(self):

        # Membuat akun Editor
        self.editor = User.objects.create_user(
            username="editor",
            password="test-password",
        )

        # Memasukkan Editor ke grup Editor
        self.editor_group, created = Group.objects.get_or_create(
            name="Editor"
        )
        self.editor.groups.add(self.editor_group)

        # Membuat akun Owner
        self.owner = User.objects.create_superuser(
            username="owner",
            password="test-password",
            email="owner@example.com",
        )

        # Membuat akun pengguna biasa
        self.visitor = User.objects.create_user(
            username="visitor",
            password="test-password",
        )

        # Membuat data Experience awal
        self.experience = Experience.objects.create(
            title="Portfolio",
            description="My experience",
            category="internship",
            thumbnail="",
            started_at=timezone.now(),
            ended_at=None,
        )

        # URL API
        self.list_url = reverse("api:experience-list")

        self.detail_url = reverse(
            "api:experience-detail",
            args=[self.experience.id],
        )

        self.star_url = reverse(
            "api:experience-star",
            args=[self.experience.id],
        )

        # Payload untuk membuat Experience
        self.payload = {
            "title": "New experience",
            "description": "A useful experience",
            "category": "internship",
            "thumbnail": "",
            "started_at": timezone.now().isoformat(),
            "ended_at": None,
        }

    # =====================================
    # 1. PUBLIC ACCESS: GET LIST AND DETAIL
    # =====================================

    def test_public_list_and_detail(self):

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data[0]["id"],
            str(self.experience.id),
        )

        self.assertEqual(
            response.data[0]["star_count"],
            0,
        )

        self.assertFalse(
            response.data[0]["is_starred"]
        )

        # Memastikan informasi sensitif tidak ditampilkan
        self.assertNotIn("email", response.data[0])
        self.assertNotIn("password", response.data[0])

        # Menguji endpoint detail
        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            str(self.experience.id),
        )

    # =====================================
    # 2. SEARCH EXPERIENCE
    # =====================================

    def test_search_and_empty_results(self):

        # Pencarian berdasarkan title
        response = self.client.get(
            self.list_url,
            {"title": "PORT"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        # Pencarian data yang tidak ditemukan
        response = self.client.get(
            self.list_url,
            {"title": "not-found"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data,
            [],
        )

    # =====================================
    # 3. ANONYMOUS VISITOR CANNOT WRITE
    # =====================================

    def test_anonymous_cannot_write_and_database_unchanged(self):

        # Pengunjung belum login
        self.assertEqual(
            Experience.objects.count(),
            1,
        )

        # Anonymous tidak boleh POST
        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Anonymous tidak boleh PATCH
        response = self.client.patch(
            self.detail_url,
            {"title": "Changed by guest"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Anonymous tidak boleh DELETE
        response = self.client.delete(
            self.detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Memastikan database tidak berubah
        self.assertEqual(
            Experience.objects.count(),
            1,
        )

        self.experience.refresh_from_db()

        self.assertEqual(
            self.experience.title,
            "Portfolio",
        )

        self.assertTrue(
            Experience.objects.filter(
                pk=self.experience.id
            ).exists()
        )

    # =====================================
    # 4. REGULAR USER CANNOT WRITE
    # =====================================

    def test_regular_user_cannot_write_and_database_unchanged(self):

        self.client.force_authenticate(
            user=self.visitor
        )

        initial_count = Experience.objects.count()

        initial_ids = set(
            Experience.objects.values_list(
                "id",
                flat=True,
            )
        )

        # User biasa tidak boleh POST
        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # User biasa tidak boleh PATCH
        response = self.client.patch(
            self.detail_url,
            {"title": "Changed by visitor"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # User biasa tidak boleh DELETE
        response = self.client.delete(
            self.detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Memastikan database tidak berubah
        self.assertEqual(
            Experience.objects.count(),
            initial_count,
        )

        current_ids = set(
            Experience.objects.values_list(
                "id",
                flat=True,
            )
        )

        self.assertEqual(
            current_ids,
            initial_ids,
        )

        self.experience.refresh_from_db()

        self.assertEqual(
            self.experience.title,
            "Portfolio",
        )

    # =====================================
    # 5. EDITOR PERMISSIONS
    # =====================================

    def test_editor_can_patch_but_cannot_create_or_delete(self):

        self.client.force_authenticate(
            user=self.editor
        )

        initial_count = Experience.objects.count()

        initial_ids = set(
            Experience.objects.values_list(
                "id",
                flat=True,
            )
        )

        # Editor boleh PATCH
        response = self.client.patch(
            self.detail_url,
            {"title": "Updated by Editor"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.experience.refresh_from_db()

        self.assertEqual(
            self.experience.title,
            "Updated by Editor",
        )

        # Editor boleh PUT
        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        # Editor tidak boleh POST
        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Database tidak bertambah
        self.assertEqual(
            Experience.objects.count(),
            initial_count,
        )

        # Editor tidak boleh DELETE
        response = self.client.delete(
            self.detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Memastikan database tetap memiliki data
        self.assertEqual(
            Experience.objects.count(),
            initial_count,
        )

        current_ids = set(
            Experience.objects.values_list(
                "id",
                flat=True,
            )
        )

        self.assertEqual(
            current_ids,
            initial_ids,
        )

        self.assertTrue(
            Experience.objects.filter(
                pk=self.experience.id
            ).exists()
        )

    # =====================================
    # 6. OWNER CAN CREATE EXPERIENCE
    # =====================================

    def test_owner_can_create_experience(self):

        self.client.force_authenticate(
            user=self.owner
        )

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        # Memastikan data benar-benar masuk database
        self.assertTrue(
            Experience.objects.filter(
                pk=response.data["id"]
            ).exists()
        )

        self.assertEqual(
            response.data["title"],
            "New experience",
        )

        self.assertEqual(
            Experience.objects.count(),
            2,
        )

    # =====================================
    # 7. OWNER CAN DELETE EXPERIENCE
    # =====================================

    def test_owner_can_delete_experience(self):

        self.client.force_authenticate(
            user=self.owner
        )

        response = self.client.delete(
            self.detail_url,
            HTTP_ACCEPT="application/json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        # Response DELETE harus kosong
        self.assertEqual(
            response.content,
            b"",
        )

        # Memastikan data benar-benar terhapus
        self.assertFalse(
            Experience.objects.filter(
                pk=self.experience.id
            ).exists()
        )

        self.assertEqual(
            Experience.objects.count(),
            0,
        )

    # =====================================
    # 8. OWNER CAN UPDATE EXPERIENCE
    # =====================================

    def test_owner_can_update_experience(self):

        self.client.force_authenticate(
            user=self.owner
        )

        response = self.client.patch(
            self.detail_url,
            {"title": "Updated by Owner"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.experience.refresh_from_db()

        self.assertEqual(
            self.experience.title,
            "Updated by Owner",
        )

    # =====================================
    # 9. VALIDATION: BLANK TITLE
    # =====================================

    def test_blank_title_is_rejected(self):

        self.client.force_authenticate(
            user=self.owner
        )

        payload = {
            **self.payload,
            "title": "   ",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "title",
            response.data,
        )

        # Data tidak boleh masuk database
        self.assertEqual(
            Experience.objects.count(),
            1,
        )

    # =====================================
    # 10. VALIDATION: BLANK DESCRIPTION
    # =====================================

    def test_blank_description_is_rejected(self):

        self.client.force_authenticate(
            user=self.owner
        )

        payload = {
            **self.payload,
            "description": "<p></p>",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "description",
            response.data,
        )

        self.assertEqual(
            Experience.objects.count(),
            1,
        )

    # =====================================
    # 11. VALIDATION: STRIP HTML TAGS
    # =====================================

    def test_html_tags_are_stripped(self):

        self.client.force_authenticate(
            user=self.owner
        )

        payload = {
            **self.payload,
            "title": "<b>New Experience</b>",
            "description": "<p>Useful Experience</p>",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["title"],
            "New Experience",
        )

        self.assertEqual(
            response.data["description"],
            "Useful Experience",
        )

        # Memastikan data bersih tersimpan di database
        experience = Experience.objects.get(
            pk=response.data["id"]
        )

        self.assertEqual(
            experience.title,
            "New Experience",
        )

        self.assertEqual(
            experience.description,
            "Useful Experience",
        )

    # =====================================
    # 12. STAR REQUIRES AUTHENTICATION
    # =====================================

    def test_star_requires_login_and_database_unchanged(self):

        # Pengunjung tanpa login mencoba memberikan star
        response = self.client.post(
            self.star_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Memastikan tidak ada star yang masuk
        self.assertEqual(
            self.experience.starred_by.count(),
            0,
        )

        # User biasa login
        self.client.force_authenticate(
            user=self.visitor
        )

        # Memberikan star
        response = self.client.post(
            self.star_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["is_starred"]
        )

        self.assertEqual(
            response.data["star_count"],
            1,
        )

        # Memastikan relasi star tersimpan di database
        self.assertTrue(
            self.experience.starred_by.filter(
                pk=self.visitor.pk
            ).exists()
        )

        # Membatalkan star
        response = self.client.post(
            self.star_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertFalse(
            response.data["is_starred"]
        )

        self.assertEqual(
            response.data["star_count"],
            0,
        )

        # Memastikan relasi star sudah terhapus
        self.assertFalse(
            self.experience.starred_by.filter(
                pk=self.visitor.pk
            ).exists()
        )

    # =====================================
    # 13. COMPUTED STAR FIELDS ARE READ ONLY
    # =====================================

    def test_computed_star_fields_are_read_only(self):

        self.client.force_authenticate(
            user=self.owner
        )

        payload = {
            **self.payload,
            "star_count": 99,
            "is_starred": True,
            "starred_by_names": "forged",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        # Nilai tidak boleh dimanipulasi melalui input
        self.assertEqual(
            response.data["star_count"],
            0,
        )

        self.assertFalse(
            response.data["is_starred"]
        )

        self.assertEqual(
            response.data["starred_by_names"],
            "",
        )

    # =====================================
    # 14. MISSING EXPERIENCE RETURNS 404
    # =====================================

    def test_missing_experience_returns_404(self):

        url = reverse(
            "api:experience-detail",
            args=[uuid.uuid4()],
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    # =====================================
    # 15. WRONG HTTP METHOD RETURNS 405
    # =====================================

    def test_wrong_method_returns_405(self):

        self.client.force_authenticate(
            user=self.owner
        )

        response = self.client.delete(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    # =====================================
    # 16. CSRF WITHOUT TOKEN IS REJECTED
    # =====================================

    def test_session_write_without_csrf_is_rejected(self):

        client = APIClient(
            enforce_csrf_checks=True
        )

        # Login menggunakan session
        self.assertTrue(
            client.login(
                username="owner",
                password="test-password",
            )
        )

        # POST tanpa CSRF token
        response = client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Memastikan database tidak berubah
        self.assertEqual(
            Experience.objects.count(),
            1,
        )

    # =====================================
    # 17. CSRF WITH TOKEN IS ACCEPTED
    # =====================================

    def test_session_write_with_csrf_succeeds(self):

        client = APIClient(
            enforce_csrf_checks=True
        )

        self.assertTrue(
            client.login(
                username="owner",
                password="test-password",
            )
        )

        # Mengakses halaman API untuk mendapatkan CSRF cookie
        page = client.get(
            self.list_url,
            HTTP_ACCEPT="text/html",
        )

        self.assertEqual(
            page.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "csrftoken",
            client.cookies,
        )

        token = client.cookies["csrftoken"].value

        # POST dengan CSRF token
        response = client.post(
            self.list_url,
            self.payload,
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        # Memastikan data berhasil tersimpan
        self.assertEqual(
            Experience.objects.count(),
            2,
        )
