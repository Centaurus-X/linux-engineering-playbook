# Safe Passwordless sudo Usage

## Scope

This guide shows how to configure limited passwordless sudo rules safely.

The old wiki note used a broad group-level `NOPASSWD: ALL` rule. This is convenient, but unsafe for general use.

> [!WARNING]
> Avoid global passwordless sudo rules such as:
>
> ```text
> %sudo ALL=(ALL:ALL) NOPASSWD: ALL
> ```
>
> This grants every sudo group member passwordless root access for every command.

## Recommended Pattern

Allow only specific commands.

Open sudoers safely:

```bash
sudo visudo
```

Add a command-specific rule:

```text
philipp ALL=(root) NOPASSWD: /usr/bin/systemctl restart rustdesk-audio.service
```

Replace:

- `philipp` with the target user.
- `/usr/bin/systemctl restart rustdesk-audio.service` with the exact command required.

## Better: Use a Drop-In File

```bash
sudo visudo -f /etc/sudoers.d/rustdesk-audio
```

Example:

```text
philipp ALL=(root) NOPASSWD: /usr/bin/systemctl restart rustdesk-audio.service, /usr/bin/systemctl status rustdesk-audio.service
```

Set permissions:

```bash
sudo chmod 0440 /etc/sudoers.d/rustdesk-audio
```

Validate:

```bash
sudo -l
```

## Safer Rules

Good:

```text
philipp ALL=(root) NOPASSWD: /usr/bin/systemctl restart rustdesk-audio.service
```

Risky:

```text
philipp ALL=(ALL:ALL) NOPASSWD: ALL
```

## Rollback

```bash
sudo rm -f /etc/sudoers.d/rustdesk-audio
sudo -l
```
