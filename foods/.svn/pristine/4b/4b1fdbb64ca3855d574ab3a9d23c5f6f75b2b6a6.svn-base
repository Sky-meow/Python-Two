from django.conf import settings
default_app_config = 'store.apps.ProjectsConfig'

if 'system' not in settings.INSTALLED_APPS:
    raise ImportError(
        "The store application requires support from the system application. "
        "Make sure you have the system application enabled"
    )

if not hasattr(settings, 'AUTH_USER_MODEL') and settings.AUTH_USER_MODEL != 'system.User':
    raise ImportError(
        "The store application requires support from the User model in system. "
        "Make sure you have the system application has the User model"
    )
