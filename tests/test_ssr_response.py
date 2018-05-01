from django.test import RequestFactory
from django_ssr_response import (
    SsrResponse,
)


request_factory = RequestFactory()


def test_response_initializes_successfully():
    request = request_factory.get('/')
    response = SsrResponse(request=request, template='dummy.html', ssr_script_path='/')
    assert response


def test_response_renders_successfully():
    request = request_factory.get('/')
    response = SsrResponse(request=request, template='dummy.html', ssr_script_path='/')
    response.render()
    assert response.status_code == 200
