# Database Design

**Engine:** MongoDB Atlas  
**ODM:** Beanie (async, Pydantic v2) — Document models live in `infrastructure/`, never in `domain/`  
**Pattern:** Event Store + State documents  
**Rule:** Events are immutable — never update or delete, only append.

---

## Collections

### `users`

Stores user accounts and roles.

```json
{
  "_id": "ObjectId",
  "email": "string (unique)",
  "password_hash": "string",
  "name": "string",
  "role": "admin | user",
  "is_active": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Roles:**

| Role | Permissions |
|------|-------------|
| `user` | Create PDDs, read own PDDs and events |
| `admin` | Read all PDDs and events, manage users (activate/deactivate, change role) |

**Indexes:**
- `email` — unique, used on login
- `role` — used by admin queries
