"""
Copyright 2026 Veil Development Team

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import http
import json
import quart
from weaver_framework.microservice.api_response import ApiResponse
from weaver_framework.microservice.base_api_route import (
    BaseApiRoute, validate_json)
from weaver_framework.microservice.http_content_type import HttpContentType
from veil.identity_service.routes.route_injections import RouteInjections
from veil.identity_service.routes.common_request_json_schema import (
    EMAIL_ADDRESS_SCHEMA, PASSWORD_SCHEMA)


SCHEMA_AUTHENTICATE_ACCOUNT_REQUEST: dict = {
    "$schema": "http://json-schema.org/draft-07/schema#",

    "type": "object",
    "additionalProperties": False,

    "properties":
    {
        "email_address": EMAIL_ADDRESS_SCHEMA,
        "password": PASSWORD_SCHEMA,
    },
    "required": ["email_address", "password"]
}


def create_blueprint(injections: RouteInjections) -> quart.Blueprint:
    """Create the authenticate account route blueprint.

    This function creates and configures the blueprint responsible
    for account authentication routes, including the POST endpoint
    used to authenticate user accounts.

    Args:
        injections: Shared route dependencies and injected services.

    Returns:
        The configured authentication account blueprint.
    """
    route = AuthenticateAccountRoute(injections)

    blueprint = quart.Blueprint('authenticate_account', __name__)

    injections.logger.debug("=> %s POST /accounts/authenticate",
                            'Authenticate an account'.ljust(40))

    @blueprint.route('/accounts/authenticate', methods=['POST'])
    async def authenticate_account_request():
        """Handle account authentication requests.

        Returns:
            The HTTP response returned by the authentication route
            handler.
        """
        # pylint: disable=no-value-for-parameter
        return await route.authenticate_account()

    return blueprint


class AuthenticateAccountRoute(BaseApiRoute):
    """Route handler for account authentication operations."""

    def __init__(self, injections: RouteInjections) -> None:
        """Initialize the authenticate account route handler.

        Args:
            injections: Shared route dependencies and injected services.
        """
        self._logger = injections.logger.getChild(__name__)
        self._injections: RouteInjections = injections

    @validate_json(SCHEMA_AUTHENTICATE_ACCOUNT_REQUEST)
    async def authenticate_account(
            self,
            request_msg: ApiResponse) -> quart.Response:
        """Authenticate an account request.

        Returns:
            A JSON HTTP response indicating the authentication
            request was processed successfully.
        """

        email_address: str = request_msg.body["email_address"].strip().lower()
        password: str = request_msg.body["password"]

        result = self._injections.account_service.authenticate_account(
            email_address=email_address,
            password=password
        )

        if result is None:
            return quart.Response(
                json.dumps({
                    "error": "invalid_credentials"
                }),
                status=http.HTTPStatus.UNAUTHORIZED,
                content_type=HttpContentType.JSON
            )

        response_body = {
            "access_token": "...",
            "expires_in": 86400,
            "user_id": "..."
        }
        return quart.Response(json.dumps(response_body),
                              status=http.HTTPStatus.OK,
                              content_type=HttpContentType.JSON)
