from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrReadOnly(BasePermission):
    message = "Only the portfolio owner can modify experiences."

    def has_permission(self, request, view):
        # Semua pengguna boleh membaca data
        if request.method in SAFE_METHODS:
            return True

        # Hanya portfolio owner (superuser) yang boleh mengubah data
        return (
            request.user.is_authenticated
            and request.user.is_superuser
        )

class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        # Semua pengguna boleh membaca.
        if request.method in SAFE_METHODS:
            return True

        # Pengguna harus login untuk melakukan perubahan.
        if not request.user.is_authenticated:
            return False

        # Superuser memiliki seluruh hak akses.
        if request.user.is_superuser:
            return True

        # Editor hanya boleh melakukan PUT dan PATCH.
        return (
            request.method in ("PUT", "PATCH")
            and request.user.groups.filter(name="Editor").exists()
        )

