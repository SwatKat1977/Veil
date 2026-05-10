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
from veil.identity_service.routes.account.register_account_route import \
    create_blueprint as register_account_blueprint


def create_account_blueprints(logger: logging.Logger) -> quart.Blueprint:
    """Create and register account-related blueprints.

    This function creates the parent account blueprint and registers
    all account management route blueprints, such as account
    registration routes.

    Args:
        logger: Logger instance used by account route handlers.

    Returns:
        The configured account blueprint containing all registered
        account-related routes.
    """
    account_blueprint = quart.Blueprint("account_routes", __name__)

    # Register account route
    account_blueprint.register_blueprint(register_account_blueprint(logger))

    return account_blueprint
