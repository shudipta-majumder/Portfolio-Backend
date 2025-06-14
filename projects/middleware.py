from django.utils import timezone 
import user_agents
from .models import RequestLog

BLOCKED_IPS = ['127.0.0.1', 'localhost','192.168.0.100', '192.168.16.124', '103.109.57.106', '58.145.187.220'] 

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        meta = request.META
        ip = meta.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[0].strip()
        else:
            ip = meta.get('REMOTE_ADDR', '0.0.0.0')
        if path.startswith('/backend/admin/') or ip in BLOCKED_IPS:
            return self.get_response(request)
        
        method = request.method
        user_agent_str = meta.get('HTTP_USER_AGENT', '')
        accept_language = meta.get('HTTP_ACCEPT_LANGUAGE', '')
        referer = request.META.get('HTTP_REFERER', '')
        timestamp = timezone.now()
        user = request.user if request.user.is_authenticated else None

        ua = user_agents.parse(user_agent_str)
        browser = ua.browser.family
        os = ua.os.family
        os_version = ua.os.version_string 
        device_type = 'Mobile' if ua.is_mobile else 'Tablet' if ua.is_tablet else 'PC'
        device_brand = ua.device.brand 
        device_family = ua.device.family
        device_model = ua.device.model 

        RequestLog.objects.create(
            user=user,
            ip_address=ip,
            path=path,
            method=method,
            user_agent=user_agent_str,
            browser=browser,
            os=f"{os} {os_version}",
            device_info=f"{device_type} {device_brand} {device_family} {device_model}",
            referer=referer,
            language=accept_language,
            accessed_at=timestamp,
        )

        return self.get_response(request)
