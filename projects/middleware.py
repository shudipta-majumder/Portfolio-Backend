from django.utils import timezone 
import user_agents
from .models import RequestLog

BLOCKED_IPS = ['127.0.0.1', '192.168.0.100', '192.168.16.124'] 

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        
        if path.startswith('/backend/admin/'):
            return self.get_response(request)
        
        if ip in BLOCKED_IPS:
            return self.get_response(request)

        meta = request.META
        ip = meta.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[0].strip()
        else:
            ip = meta.get('REMOTE_ADDR', '0.0.0.0')
        method = request.method
        user_agent_str = meta.get('HTTP_USER_AGENT', '')
        accept_language = meta.get('HTTP_ACCEPT_LANGUAGE', '')
        timestamp = timezone.now()
        user = request.user if request.user.is_authenticated else None

        ua = user_agents.parse(user_agent_str)
        browser = ua.browser.family
        os = ua.os.family
        device_type = 'Mobile' if ua.is_mobile else 'Tablet' if ua.is_tablet else 'PC'

        RequestLog.objects.create(
            user=user,
            ip_address=ip,
            path=path,
            method=method,
            user_agent=user_agent_str,
            browser=browser,
            os=os,
            device_type=device_type,
            language=accept_language,
            accessed_at=timestamp,
        )

        return self.get_response(request)
