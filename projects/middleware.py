from django.utils import timezone 
import user_agents
from .models import RequestLog

BLOCKED_IPS = ['127.0.0.1', 'localhost','192.168.0.100', '103.92.84.16', '103.109.57.106'] 

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        meta = request.META
        x_forwarded_for = meta.get('HTTP_X_FORWARDED_FOR')
       
        if x_forwarded_for:
            ip_list = [ip.strip() for ip in x_forwarded_for.split(',')]
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip_list = [request.META.get('REMOTE_ADDR', '0.0.0.0')]
            ip = meta.get('REMOTE_ADDR', '0.0.0.0')
            
        if any(ip in BLOCKED_IPS for ip in ip_list):
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
            ip_addresses=ip_list,
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
