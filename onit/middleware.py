from django.conf import settings


class DynamicAllowedHostsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract X-Forwarded-Host from headers
        forwarded_host = request.META.get('HTTP_X_FORWARDED_HOST')

        if forwarded_host:
            # If present, append it to the ALLOWED_HOSTS list
            allowed_hosts = list(settings.ALLOWED_HOSTS)
            allowed_hosts.append(forwarded_host)
            # Dynamically update ALLOWED_HOSTS for the request
            request._allowed_hosts = allowed_hosts

        response = self.get_response(request)
        return response
