import logging
import quart
from veil.identity_service.routes.auth.authenticate_route import \
    create_blueprint as create_authenticate_account_blueprint
from veil.identity_service.routes.auth.logout_route import \
    create_blueprint as create_logout_blueprint


def create_auth_blueprints(logger: logging.Logger) -> quart.Blueprint:
    account_blueprint = quart.Blueprint("account_routes", __name__)

    # Authenticate account route
    account_blueprint.register_blueprint(
        create_authenticate_account_blueprint(logger))

    # Logout account route
    account_blueprint.register_blueprint(create_logout_blueprint(logger))

    return account_blueprint
