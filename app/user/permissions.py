from rest_framework.permissions import IsAuthenticated


class IsActive(IsAuthenticated):
    """
    Allows access only for active users.
    """
    def has_permission(self, request, view) -> bool:
        return super().has_permission(request, view) and request.user.is_active
