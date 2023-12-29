from typing import TYPE_CHECKING, Dict, Optional, Sequence, Tuple, Type

from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


def get_auth_header(headers: Dict[str, str]) -> Optional[Tuple[str, str]]:

    """
    Extracts and parses the Authorization header from the given HTTP headers.

    :param: headers (dict): Dictionary containing HTTP headers.

    :return: Optional[Tuple[str, str]]: Tuple containing the authentication
        type and value, or None if the Authorization header is missing or invalid.
    """

    value = headers.get('Authorization')

    if not value:
        return None

    try:
        auth_type, auth_value = value.split()[:2]
        return auth_type, auth_value
    except (ValueError, IndexError):
        return None


if TYPE_CHECKING:
    # This is going to be resolved in the stub library
    # https://github.com/typeddjango/djangorestframework-stubs/
    from rest_framework.permissions import _PermissionClass

    PermissionClassesType = Sequence[_PermissionClass]
else:
    PermissionClassesType = Sequence[Type[BasePermission]]


class ApiAuthMixin:
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
            JWTAuthentication,
    ]
    permission_classes: PermissionClassesType = (IsAuthenticated, )
