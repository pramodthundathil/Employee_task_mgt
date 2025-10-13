# middleware.py
import threading

_thread_locals = threading.local()

def get_current_user():
    """Get the current user from thread local storage"""
    return getattr(_thread_locals, 'user', None)

def set_current_user(user):
    """Set the current user in thread local storage"""
    _thread_locals.user = user

class ThreadLocalUserMiddleware:
    """
    Middleware to store current user in thread local storage.
    Add this to MIDDLEWARE in settings.py
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Store user in thread local
        set_current_user(getattr(request, 'user', None))
        
        try:
            response = self.get_response(request)
        finally:
            # Clean up after request
            set_current_user(None)
        
        return response