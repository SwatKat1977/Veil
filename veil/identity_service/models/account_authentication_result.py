from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class AccountAuthenticationResult:
    """Successful authentication result."""

    account_id: int
    user_id: str
    display_name: str
