from rest_framework.permissions import BasePermission

class IsInGroup(BasePermission):
    group_names = []  # To be defined in subclasses

    def has_object_permission(self, request, view, obj):
        return any(request.user.groups.filter(name=group_name).exists() for group_name in self.group_names)
    
    def has_permission(self, request, view):
        return any(request.user.groups.filter(name=group_name).exists() for group_name in self.group_names)

# Subclasses for each group:
class IsAdminUser(IsInGroup):
    group_names = ["admin"]

class IsRegularUser(IsInGroup):
    group_names = ["users"]

class IsEditorUser(IsInGroup):
    group_names = ["editors"]

class IsAdminOrEditorUser(IsInGroup):
    group_names = ["admin", "editors"]
