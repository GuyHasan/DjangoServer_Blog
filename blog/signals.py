from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, User
from django.dispatch import receiver

@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    """
    This function runs automatically after migrations are applied.
    It ensures default groups and a superuser exist.
    """

    if sender.name == "users":  # Only run this for the 'users' app migrations
        group_names = ["admin", "users", "editors"]
        for group_name in group_names:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                print(f"✅ Created group: {group_name}")

        # Create a default superuser if it doesn't exist
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "adminpassword")
            print("✅ Created default superuser: admin")
