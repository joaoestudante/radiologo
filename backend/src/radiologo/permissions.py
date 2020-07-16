from rest_framework.permissions import BasePermission

from programs.models import Program

allowed_read_methods = ("GET", "HEAD", "OPTIONS")
allowed_write_methods = ("GET", "HEAD", "OPTIONS", "POST", "PUT", "DELETE")


class IsProgrammingR(BasePermission):
    def has_permission(self, request, view):
        if request.user.department == "PR" and request.method in allowed_read_methods:
            return True
        return False


class IsProgrammingRW(BasePermission):
    def has_permission(self, request, view):
        if request.user.department == "PR" and request.method in allowed_write_methods:
            return True
        return False


class IsTechnicalLogisticR(BasePermission):
    def has_permission(self, request, view):
        if request.user.department == "TL" and request.method in allowed_read_methods:
            return True
        return False


class IsTechnicalLogisticRW(BasePermission):
    def has_permission(self, request, view):
        if request.user.department == "TL" and request.method in allowed_write_methods:
            return True
        return False


class IsCommunicationMarketingR(BasePermission):
    def has_permission(self, request, view):
        if request.user.department == "CM" and request.method in allowed_read_methods:
            return True
        return False


class IsCommunicationMarketingRW(BasePermission):
    def has_permission(self, request, view):
        if request.user.department == "CM" and request.method in allowed_write_methods:
            return True
        return False


class IsAdministration(BasePermission):
    def has_permission(self, request, view):
        if request.user.department == "AD":
            return True
        return False


class IsDirector(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == "DI":
            return True
        return False


class IsProgramOwner(BasePermission):
    def has_permission(self, request, view):
        requested_program = Program.objects.get(pk=view.kwargs["pk"])
        if request.user in list(requested_program.authors.all()):
            return True
        return False


class IsRadiologoDeveloper(BasePermission):
    def has_permission(self, request, view):
        devs = ["João Lourenço", "Ricardo Maçãs"]
        if request.user.author_name in devs:
            return True
        return False
