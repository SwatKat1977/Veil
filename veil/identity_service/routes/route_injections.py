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
from dataclasses import dataclass
import logging
from veil.identity_service.services.account_service import AccountService


@dataclass(slots=True, frozen=True)
class RouteInjections:
    """Container for dependencies injected into route handlers.

    Attributes:
        logger: Logger instance used for route-level logging and diagnostics.
    """

    logger: logging.Logger
    account_service: AccountService
