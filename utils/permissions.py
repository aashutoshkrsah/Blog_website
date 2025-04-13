from django.contrib.auth.models import Group

def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

def is_editor(user):
    return has_group(user, "Editor")

def is_manager(user):
    return has_group(user, "Manager")

def is_reader(user):
    return has_group(user, "Reader")

def is_custom_superuser(user):
    return has_group(user, "Superuser")  # your custom group

def is_superuser(user):
    return user.is_superuser or is_custom_superuser(user)
