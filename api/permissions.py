from rest_framework.permissions import BasePermission
from .models import Company

class IsAdminUser(BasePermission):
    """
    Custom permission to only allow admins to access the view.
    """
    def has_permission(self, request, view):
        try:
            company = Company.objects.get(user=request.user)
            return company.role == Company.Role.ADMIN
        except (Company.DoesNotExist, AttributeError):
            return False

