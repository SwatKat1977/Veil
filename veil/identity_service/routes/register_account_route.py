import http
import json
import logging
import quart
from veil.common.base_api_route import BaseApiRoute


def create_blueprint(logger: logging.Logger) -> quart.Blueprint:
    new_route = RegisterAccountRoute(logger)

    blueprint = quart.Blueprint('register_account', __name__)

    logger.debug("=> %s POST /accounts/register",
                 'Register new account'.ljust(30))

    @blueprint.route('/accounts/register', methods=['POST'])
    async def register_account_request():
        return await new_route.register_account()

    return blueprint


class RegisterAccountRoute(BaseApiRoute):
    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger.getChild(__name__)

    async def register_account(self) -> quart.Response:
        return quart.Response(json.dumps({}),
                              status=http.HTTPStatus.OK,
                              content_type=self.CONTENT_TYPE_JSON)
