from rest_framework.permissions import BasePermission

class IsInGroup(BasePermission):
    """
    Allows access only to users in a specific group.
    """
    group_name = None  # To be defined in subclasses

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="admin").exists():
            return True  
        if request.user == obj.owner:
            return True 
        return False  

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False  
        return request.user.groups.filter(name=self.group_name).exists()
    
    


# Subclasses for each group:
class IsAdminUser(IsInGroup):
    group_name = "admin"

class IsEditorUser(IsInGroup):
    group_name = "editors"

class IsRegularUser(IsInGroup):
    group_name = "users"
