default_app_config = 'order.apps.OrderConfig'

from django.conf import settings
if 'customer' not in settings.INSTALLED_APPS:
    raise ImportError(
            "The order application requires support from the customer application. "
            "Make sure you have the customer application enabled"
    )

if 'material' not in settings.INSTALLED_APPS:
    raise ImportError(
            "The order application requires support from the material application. "
            "Make sure you have the material application enabled"
    )

if 'store' not in settings.INSTALLED_APPS:
    raise ImportError(
            "The order application requires support from the store application. "
            "Make sure you have the store application enabled"
    )