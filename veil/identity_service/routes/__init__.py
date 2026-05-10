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
from veil.identity_service.routes.account import create_account_blueprints
from veil.identity_service.routes.auth import create_auth_blueprints
from veil.identity_service.routes.system import create_system_blueprints


def create_blueprints(logger: logging.Logger) -> quart.Blueprint:
    """Create and register all API route blueprints.

    This function creates the root API blueprint and registers all
    child blueprints for the identity service, including account
    management and authentication routes.

    Args:
        logger: Logger instance used by route handlers throughout
            the API.

    Returns:
        The configured root API blueprint containing all registered
        API routes.
    """
    api_routes = quart.Blueprint("api_routes", __name__)

    # Account routes
    api_routes.register_blueprint(create_account_blueprints(logger))

    # Account authentication routes
    api_routes.register_blueprint(create_auth_blueprints(logger))

    # Systems routes
    api_routes.register_blueprint(create_system_blueprints(logger))

    return api_routes
