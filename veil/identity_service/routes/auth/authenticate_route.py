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
import logging
import quart
from veil.common.base_api_route import BaseApiRoute


def create_blueprint(logger: logging.Logger) -> quart.Blueprint:
    route = AuthenticateAccountRoute(logger)

    blueprint = quart.Blueprint('authenticate_account', __name__)

    logger.debug("=> %s POST /accounts/authenticate",
                 'Authenticate an account'.ljust(40))

    @blueprint.route('/accounts/authenticate', methods=['POST'])
    async def authenticate_account_request():
        return await route.authenticate_account()

    return blueprint


class AuthenticateAccountRoute(BaseApiRoute):

    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger.getChild(__name__)

    async def authenticate_account(self) -> quart.Response:
        return quart.Response(json.dumps({}),
                              status=http.HTTPStatus.OK,
                              content_type=self.CONTENT_TYPE_JSON)
