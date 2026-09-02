from .models import StoreSettings

def global_settings(request):
    try:
        settings = StoreSettings.load()
        return {'store_settings': settings}
    except Exception:
        # Fallback if db is not ready
        return {}
