"""http helpers"""
from os import environ
from typing import Any, Optional

from django.http import HttpRequest
from requests.sessions import Session
from sentry_sdk.hub import Hub
from structlog.stdlib import get_logger

from authentik import ENV_GIT_HASH_KEY, __version__

OUTPOST_REMOTE_IP_HEADER = "HTTP_X_AUTHENTIK_REMOTE_IP"
OUTPOST_TOKEN_HEADER = "HTTP_X_AUTHENTIK_OUTPOST_TOKEN"  # nosec
DEFAULT_IP = "255.255.255.255"
LOGGER = get_logger()


def _get_client_ip_from_meta(meta: dict[str, Any]) -> str:
    """Attempt to get the client's IP by checking common HTTP Headers.
    Returns none if no IP Could be found"""
    headers = (
        "HTTP_X_FORWARDED_FOR",
        "HTTP_X_REAL_IP",
        "REMOTE_ADDR",
    )
    for _header in headers:
        if _header in meta:
            ips: list[str] = meta.get(_header).split(",")
            return ips[0].strip()
    return DEFAULT_IP


def _get_outpost_override_ip(request: HttpRequest) -> Optional[str]:
    """Get the actual remote IP when set by an outpost. Only
    allowed when the request is authenticated, by a user with USER_ATTRIBUTE_CAN_OVERRIDE_IP set
    to outpost"""
    from authentik.core.models import USER_ATTRIBUTE_CAN_OVERRIDE_IP, Token, TokenIntents

    if OUTPOST_REMOTE_IP_HEADER not in request.META or OUTPOST_TOKEN_HEADER not in request.META:
        return None
    fake_ip = request.META[OUTPOST_REMOTE_IP_HEADER]
    tokens = Token.filter_not_expired(
        key=request.META.get(OUTPOST_TOKEN_HEADER), intent=TokenIntents.INTENT_API
    )
    if not tokens.exists():
        LOGGER.warning("Attempted remote-ip override without token", fake_ip=fake_ip)
        return None
    user = tokens.first().user
    if not user.group_attributes().get(USER_ATTRIBUTE_CAN_OVERRIDE_IP, False):
        LOGGER.warning(
            "Remote-IP override: user doesn't have permission",
            user=user,
            fake_ip=fake_ip,
        )
        return None
    # Update sentry scope to include correct IP
    user = Hub.current.scope._user
    if not user:
        user = {}
    user["ip_address"] = fake_ip
    Hub.current.scope.set_user(user)
    return fake_ip


def get_client_ip(request: Optional[HttpRequest]) -> str:
    """Attempt to get the client's IP by checking common HTTP Headers.
    Returns none if no IP Could be found"""
    if not request:
        return DEFAULT_IP
    override = _get_outpost_override_ip(request)
    if override:
        return override
    return _get_client_ip_from_meta(request.META)


def authentik_user_agent() -> str:
    """Get a common user agent"""
    build = environ.get(ENV_GIT_HASH_KEY, "tagged")
    return f"authentik@{__version__} (build={build})"


def get_http_session() -> Session:
    """Get a requests session with common headers"""
    session = Session()
    session.headers["User-Agent"] = authentik_user_agent()
    return session
