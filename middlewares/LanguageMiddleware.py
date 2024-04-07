from django.utils.translation import activate
from django.utils.deprecation import MiddlewareMixin

class SetLanguageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        language = request.headers.get('Accept-Language', 'ar')  # Default to Arabic if not specified
        activate(language)
