# PostgreSQL LISTEN/NOTIFY

## Scope

This guide creates PostgreSQL triggers that emit JSON notifications through PostgreSQL `NOTIFY`.

This is useful for dashboards, WebSocket gateways, audit systems, and event-driven integration.

## Concept

```text
Table change
    └─ AFTER INSERT / UPDATE / DELETE trigger
        └─ pg_notify(channel, json_payload)
            └─ listener receives event
```

## 1. Create a Trigger Function

Example schema:

```sql
CREATE SCHEMA IF NOT EXISTS websocket_database;
```

Trigger function:

```sql
CREATE OR REPLACE FUNCTION websocket_database.notify_trigger_function_after()
RETURNS TRIGGER AS $$
DECLARE
    payload JSON;
BEGIN
    payload := json_build_object(
        'schema', TG_TABLE_SCHEMA,
        'table', TG_TABLE_NAME,
        'action', TG_OP,
        'data', CASE
            WHEN TG_OP = 'DELETE' THEN row_to_json(OLD)
            ELSE row_to_json(NEW)
        END
    );

    PERFORM pg_notify('notify_' || TG_TABLE_NAME, payload::text);

    IF TG_OP = 'DELETE' THEN
        RETURN OLD;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

## 2. Attach Trigger to a Table

Example:

```sql
CREATE TRIGGER after_devices_action
AFTER INSERT OR UPDATE OR DELETE
ON websocket_database.devices
FOR EACH ROW
EXECUTE FUNCTION websocket_database.notify_trigger_function_after();
```

## 3. Listen for Notifications

In `psql`:

```sql
LISTEN notify_devices;
```

Then modify the table:

```sql
INSERT INTO websocket_database.devices (name) VALUES ('test-device');
```

## 4. Important Commands

| Command | Purpose |
|---|---|
| `LISTEN channel_name;` | Subscribe to a notification channel |
| `UNLISTEN channel_name;` | Unsubscribe from a channel |
| `NOTIFY channel_name, 'payload';` | Send a manual notification |
| `pg_notify(channel, payload)` | Send a notification from SQL/PLpgSQL |

## 5. Production Notes

- Keep payloads compact.
- Treat `NOTIFY` as a signal, not as a durable message queue.
- Use a transaction log table when events must not be lost.
- Keep channel names stable and documented.
- Test trigger behavior for `DELETE`, because `NEW` is not available for delete operations.

## Rollback

```sql
DROP TRIGGER IF EXISTS after_devices_action ON websocket_database.devices;
DROP FUNCTION IF EXISTS websocket_database.notify_trigger_function_after();
```
