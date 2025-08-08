from django.apps import AppConfig
from django.db.models.signals import post_migrate

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        post_migrate.connect(create_groups, sender=self)


def create_groups(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from reviews.models import Review
    from users.models import CustomUser

    group, _ = Group.objects.get_or_create(name='StaffAdmins')

    review_ct = ContentType.objects.get_for_model(Review)
    user_ct = ContentType.objects.get_for_model(CustomUser)

    perms = Permission.objects.filter(
        content_type__in=[review_ct, user_ct]
    )

    group.permissions.set(perms)

