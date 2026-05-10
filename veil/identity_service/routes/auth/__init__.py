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
import logging
import quart
from veil.identity_service.routes.auth.authenticate_route import \
    create_blueprint as create_authenticate_account_blueprint
from veil.identity_service.routes.auth.logout_route import \
    create_blueprint as create_logout_blueprint


def create_auth_blueprints(logger: logging.Logger) -> quart.Blueprint:
    """Create and register authentication-related blueprints.

    This function creates the parent authentication blueprint and registers
    all authentication route blueprints, including account authentication
    and logout routes.

    Args:
        logger: Logger instance used by authentication route handlers.

    Returns:
        The configured authentication blueprint containing all registered
        authentication routes.
    """
    account_blueprint = quart.Blueprint("account_routes", __name__)

    # Authenticate account route
    account_blueprint.register_blueprint(
        create_authenticate_account_blueprint(logger))

    # Logout account route
    account_blueprint.register_blueprint(create_logout_blueprint(logger))

    return account_blueprint
