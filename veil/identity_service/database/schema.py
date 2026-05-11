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
SCHEMA_VERSION = 1

CREATE_SCHEMA_METADATA_TABLE = """
CREATE TABLE IF NOT EXISTS schema_metadata (
    schema_version INTEGER NOT NULL
);
"""

CREATE_ACCOUNTS_TABLE = """
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL UNIQUE,

    email_address TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL UNIQUE,

    password_hash TEXT NOT NULL,

    is_validated INTEGER NOT NULL DEFAULT 0 CHECK (is_validated IN (0, 1)),
    is_disabled INTEGER NOT NULL DEFAULT 0 CHECK (is_disabled IN (0, 1)),

    failed_login_attempts INTEGER NOT NULL DEFAULT 0,

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login_at TEXT DEFAULT NULL
);
"""

CREATE_ROLES_TABLE = """
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    role_name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL
);
"""

CREATE_ACCOUNT_ROLES_TABLE = """
CREATE TABLE IF NOT EXISTS account_roles (
    account_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,

    PRIMARY KEY (account_id, role_id),

    FOREIGN KEY (account_id)
        REFERENCES accounts(id)
        ON DELETE CASCADE,

    FOREIGN KEY (role_id)
        REFERENCES roles(id)
        ON DELETE CASCADE
);
"""

# Indexes

CREATE_ACCOUNT_EMAIL_INDEX = """
CREATE INDEX IF NOT EXISTS idx_accounts_email
ON accounts(email_address);
"""

CREATE_ACCOUNT_DISPLAY_NAME_INDEX = """
CREATE INDEX IF NOT EXISTS idx_accounts_display_name
ON accounts(display_name);
"""

CREATE_ROLE_NAME_INDEX = """
CREATE INDEX IF NOT EXISTS idx_roles_role_name
ON roles(role_name);
"""

# Default seed data

DEFAULT_ROLES = [
    (
        "admin",
        "Platform administrator with unrestricted access"
    ),
    (
        "player",
        "Standard interactive Veil user"
    ),
    (
        "observer",
        "Restricted viewing account"
    )
]

TABLE_SCHEMA_QUERIES = [
    CREATE_SCHEMA_METADATA_TABLE,
    CREATE_ACCOUNTS_TABLE,
    CREATE_ROLES_TABLE,
    CREATE_ACCOUNT_ROLES_TABLE
]

INDEX_SCHEMA_QUERIES = [
    CREATE_ACCOUNT_EMAIL_INDEX,
    CREATE_ACCOUNT_DISPLAY_NAME_INDEX,
    CREATE_ROLE_NAME_INDEX
]

INSERT_SCHEMA_VERSION = """
INSERT INTO schema_metadata (schema_version)
VALUES (?);
"""

INSERT_ROLE = """
INSERT OR IGNORE INTO roles (role_name, description)
VALUES (?, ?);
"""

GET_SCHEMA_VERSION = """
SELECT schema_version
FROM schema_metadata
LIMIT 1;
"""

GET_ACCOUNT_BY_EMAIL = """
SELECT id
FROM accounts
WHERE email_address = ?;
"""

INSERT_ACCOUNT = """
INSERT INTO accounts (
    user_id,
    email_address,
    display_name,
    password_hash,
    is_validated,
    is_disabled
)
VALUES (?, ?, ?, ?, ?, ?);
"""

GET_ROLE_ID_BY_NAME = """
SELECT id
FROM roles
WHERE role_name = ?;
"""

INSERT_ACCOUNT_ROLE = """
INSERT INTO account_roles (
    account_id,
    role_id
)
VALUES (?, ?);
"""

GET_ACCOUNT_BY_USER_ID = """
SELECT *
FROM accounts
WHERE user_id = ?;
"""
