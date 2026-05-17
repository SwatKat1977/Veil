# Database Schema

## accounts

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `TEXT` | Primary Key | Unique account identifier |
| `display_name` | `TEXT` | `NOT NULL` | User display name |
| `email_address` | `TEXT` | `NOT NULL`, `UNIQUE` | User email address |
| `password_hash` | `TEXT` | `NOT NULL` | Hashed user password |
| `role` | `TEXT` | `NOT NULL`, Default: `'user'` | Account role |
| `validated` | `INTEGER` | `NOT NULL`, Default: `0` | Whether the account has been validated |
| `created_at` | `TEXT` | `NOT NULL` | Account creation timestamp |
| `updated_at` | `TEXT` | `NOT NULL` | Last account update timestamp |

### Example SQL

```sql
CREATE TABLE accounts (
    id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    email_address TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    validated INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

---

## roles

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `TEXT` | Primary Key | Unique role identifier |
| `role_name` | `TEXT` | `NOT NULL` | Name of the role |

### Example SQL

```sql
CREATE TABLE roles (
    id TEXT PRIMARY KEY,
    role_name TEXT NOT NULL
);
```
