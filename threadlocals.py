#       -*- coding: utf-8 -*-
try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()


def get_current_user():
    return getattr(_thread_locals, 'user', None)


def get_current_site():
    return getattr(_thread_locals, 'site', None)


def get_current_session():
    return getattr(_thread_locals, 'session', None)


def get_app_label():
    return getattr(_thread_locals, 'app_label', None)


def get_model_name():
    return getattr(_thread_locals, 'model_name', None)


def get_path():
    return getattr(_thread_locals, 'path', None)


def get_params():
    return getattr(_thread_locals, 'params', None)


def get_post_data():
    return getattr(_thread_locals, 'post_data', None)


def get_request_method():
    return getattr(_thread_locals, 'request_method', None)


def get_request():
    return getattr(_thread_locals, 'request', None)


class ThreadLocals(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""

    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)
        _thread_locals.site = getattr(request, 'site', None)
        _thread_locals.session = getattr(request, 'session', None)
        _thread_locals.path = getattr(request, 'path', None)
        _thread_locals.params = getattr(request, 'GET', None)
        _thread_locals.post_data = getattr(request, 'POST', None)
        _thread_locals.request_method = getattr(request, 'method', None)
        _thread_locals.request = request

