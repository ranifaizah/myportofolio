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
