"""Explicit, bounded release metadata query; never install or download code."""
import json
import urllib.request
from packaging.version import Version, InvalidVersion

ENDPOINT = 'https://api.github.com/repos/dhtfish-98/ImageQuay/releases/latest'
RELEASE_ROOT = 'https://github.com/dhtfish-98/ImageQuay/releases/tag/'
MAX_RESPONSE_BYTES = 1 << 20


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, url):
        raise ValueError('release metadata redirects are not allowed')


def read_release(current_version, opener=None):
    """Only called following --check-updates or a direct caller request."""
    request = urllib.request.Request(ENDPOINT, headers={'Accept':'application/vnd.github+json', 'User-Agent':'ImageQuay-update-metadata'})
    open_request = opener or urllib.request.build_opener(_NoRedirect()).open
    try:
        with open_request(request, timeout=3) as response:
            data = response.read(MAX_RESPONSE_BYTES + 1)
        if len(data) > MAX_RESPONSE_BYTES:
            raise ValueError('release metadata exceeds the 1 MiB budget')
        document = json.loads(data)
        tag = document['tag_name']
        url = document['html_url']
        if not isinstance(tag, str) or not isinstance(url, str) or url != RELEASE_ROOT + tag:
            raise ValueError('release metadata has an unexpected repository URL')
        if Version(tag.lstrip('v')) > Version(current_version):
            return url
        return None
    except (OSError, ValueError, KeyError, TypeError, InvalidVersion):
        return None
