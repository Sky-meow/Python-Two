from django.conf import settings
default_app_config = 'custrole.apps.CustroleConfig'

if 'customer' not in settings.INSTALLED_APPS:
    raise ImportError(
        "The custrole application requires support from the customer application. "
        "Make sure you have the customer application enabled"
    )
