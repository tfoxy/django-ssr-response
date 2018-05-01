# -*- coding: utf-8 -*-
import re

# from django.conf import settings
from django.template.context_processors import csrf
from django.template.response import TemplateResponse
from django.utils.six.moves import http_cookies
from react.render import render_component


class SsrResponseMixin(object):
    def __init__(
        self,
        request,
        template,
        ssr_script_path,
        ssr_client_manifest_path='',
        ssr_router_base_url='',
        application=None,
        *args,
        **kwargs
    ):
        self.ssr_script_path = ssr_script_path
        self.ssr_client_manifest_path = ssr_client_manifest_path
        self.ssr_router_base_url = ssr_router_base_url
        self._application = application
        super(SsrResponseMixin, self).__init__(
            request=request,
            template=template,
            *args,
            **kwargs
        )

    def resolve_context(self, context):
        if not context:
            context = {}
        if 'ssr' not in context:
            context['ssr'] = self.get_ssr_context_data()
            context['ssr_router_base_url'] = self.ssr_router_base_url
        return super(SsrResponseMixin, self).resolve_context(context)

    def get_ssr_context_data(self):
        ssr_context = render_component(self.ssr_script_path, {
            'clientManifest': self.ssr_client_manifest_path,
            'requestConfig': {
                'baseURL': self._get_ssr_base_url(),
                'headers': self._get_ssr_http_headers(),
            },
            'url': self._get_ssr_router_url(),
        }).markup
        return ssr_context

    def _get_ssr_http_headers(self):
        self._set_request_cookies_from_response()
        regex = re.compile('^HTTP_')
        http_headers = dict(
            (regex.sub('', header), value)
            for (header, value) in self._request.META.items()
            if header.startswith('HTTP_')
        )
        http_headers['ACCEPT'] = '*/*'
        http_headers['REFERER'] = self._request.build_absolute_uri()
        http_headers['X-CSRFToken'] = \
            unicode(csrf(self._request)['csrf_token'])
        return http_headers

    def _get_ssr_base_url(self):
        if 'werkzeug.request' in self._request.META:
            return self._request.META['werkzeug.request'].host_url
        else:
            return 'http://localhost:{}'.format(
                self._request.META['SERVER_PORT'],
            )

    def _get_ssr_router_url(self):
        base_url = self.ssr_router_base_url
        url = self._request.path
        if base_url and url.startswith(base_url):
            base_url_len = len(base_url)
            if base_url.endswith('/'):
                base_url_len -= 1
            url = url[base_url_len:]
        return url

    def _get_response_cookies(self):
        if not self._application:
            return {}
        from django.http.response import HttpResponse
        response = HttpResponse()
        for middleware_method in self._application._response_middleware:
            response = middleware_method(self._request, response)
            # Complain if the response middleware returned None (a common error).
            if response is None:
                raise ValueError(
                    "%s.process_response didn't return an "
                    "HttpResponse object. It returned None instead."
                    % (middleware_method.__self__.__class__.__name__))
        return response.cookies

    def _set_request_cookies_from_response(self):
        request_cookies = self._request.COOKIES
        response_cookies = self._get_response_cookies()
        response_cookies_dict = dict(
            (k, v.value) for k, v in response_cookies.items(),
        )
        request_cookies.update(response_cookies_dict)
        meta_cookies = '; '.join(
            '{}={}'.format(
                c[0], http_cookies._quote(c[1])
            ) for c in request_cookies.items()
        )
        self._request.META['HTTP_COOKIE'] = meta_cookies
        self.cookies.update(response_cookies)


class SsrResponse(SsrResponseMixin, TemplateResponse):
    pass
