from django.contrib.auth.models import User, Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from articles.models import Article  
from comments.models import Comment  

@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    """
    This function runs automatically after migrations are applied.
    It ensures default groups, users, articles, and comments exist.
    """
    # Dictionary to store user objects for later use
    users = {}

    if sender.name == "users":  # Only run this for the 'users' app migrations
        group_names = ["admin", "users", "editors"]
        groups = {}  

        # Create groups
        for group_name in group_names:
            group, created = Group.objects.get_or_create(name=group_name)
            groups[group_name] = group  # Store for later use
            if created:
                print(f"Created group: {group_name}")

        # Create users and assign to groups
        users_data = [
            {"username": "admin_user", "email": "admin@example.com", "password": "adminpassword", "group": "admin"},
            {"username": "editor_user", "email": "editor@example.com", "password": "editorpassword", "group": "editors"},
            {"username": "regular_user", "email": "user@example.com", "password": "userpassword", "group": "users"},
        ]

        for user_data in users_data:
            user, created = User.objects.get_or_create(username=user_data["username"], email=user_data["email"])
            if created:
                user.set_password(user_data["password"])  # Hash password
                user.save()
                user.groups.add(groups[user_data["group"]])  # Assign to group
                print(f"Created user: {user.username} in group {user_data['group']}")
            users[user_data["group"]] = user  # Store user object

        # After users are created, create articles
        articles_data = [
            {"title": "Admin's Article", "content": "This is an article by the admin.", "author": users["admin"]},
            {"title": "Editor's Article", "content": "This is an article by the editor.", "author": users["editors"]},
        ]
        articles = []
        for article_data in articles_data:
            article, created = Article.objects.get_or_create(title=article_data["title"], defaults=article_data)
            if created:
                print(f"Created article: {article.title}")
            articles.append(article)

        # After articles are created, create comments
        for article in articles:
            for user in users.values():
                Comment.objects.get_or_create(
                    article=article, author=user, content=f"This is a comment by {user.username}."
                )
                print(f"Created comment by {user.username} on {article.title}")
