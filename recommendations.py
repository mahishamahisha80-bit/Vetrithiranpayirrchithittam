from .gemini import GeminiService
from .fallback import home_fallback, party_fallback, jewelry_fallback

service = GeminiService()

def generate_home(data):
    try:
        if service.available:
            return service.generate("home", data.model_dump()).model_dump()
    except Exception:
        pass
    return home_fallback(data)

def generate_party(data):
    try:
        if service.available:
            return service.generate("party", data.model_dump()).model_dump()
    except Exception:
        pass
    return party_fallback(data)

def generate_jewelry(data, image_bytes=None, mime_type=None):
    try:
        if service.available:
            return service.generate("jewelry", data.model_dump(), image_bytes, mime_type).model_dump()
    except Exception:
        pass
    return jewelry_fallback(data)
