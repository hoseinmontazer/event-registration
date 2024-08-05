import time
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)

class RequestResponseLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request:
            request_data = {
                "RequesTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "method": request.method,
                "url": request.get_full_path(),
                "user_address": request.META.get("REMOTE_ADDR"),
            }
            #current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            logger.info(f"Incoming request: {request_data}")

    def process_response(self, request, response):
        response_data = {
            "RequesTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "status_code": response.status_code,
            "response_content": response.content.decode("utf-8")
        }
        #current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logger.info(f"Outgoing response: {response_data}")
        return response