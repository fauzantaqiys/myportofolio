from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrReadOnly(BasePermission):
    """
    Izin untuk bagian Tutorial (Experience):
    - Metode aman (GET, HEAD, OPTIONS) diizinkan untuk semua pengunjung.
    - Operasi tulis (POST, PUT, PATCH, DELETE) hanya diizinkan untuk superuser/pemilik portofolio.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and request.user.is_superuser
        )


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """
    Izin untuk bagian Tugas (Interest):
    - Metode aman diizinkan untuk semua pengunjung.
    - Superuser diizinkan semua aksi tulis.
    - Editor diizinkan aksi pembaruan (PUT, PATCH).
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return (
            request.method in ("PUT", "PATCH")
            and request.user.groups.filter(name="Editor").exists()
        )
