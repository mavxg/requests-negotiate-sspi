import requests

__all__ = ['requests_negotiate_sspi']
from .requests_negotiate_sspi import HttpNegotiateAuth  # noqa

# Monkeypatch urllib3 to expose the peer certificate
HTTPAdapter = requests.adapters.HTTPAdapter
orig_HTTPAdapter_build_response = HTTPAdapter.build_response


def new_HTTPAdapter_build_response(self, request, resp):
    response = orig_HTTPAdapter_build_response(self, request, resp)
    try:
        response.peercert = resp._connection.sock.getpeercert(binary_form=True)
    except AttributeError:
        response.peercert = None
    return response


HTTPAdapter.build_response = new_HTTPAdapter_build_response
