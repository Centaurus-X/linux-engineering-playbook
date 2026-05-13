# Keyboard Lock Python Notes

## Scope

This is an experimental note about locking and unlocking keyboard input for local lab systems.

> [!WARNING]
> Keyboard locking can make a machine difficult to recover remotely.
> Test only on systems where you have console or remote recovery access.

## Linux / X11 Concept

The old note used `xinput` to detach a keyboard device.

This approach is X11-specific and may not work on Wayland.

List input devices:

```bash
xinput --list
```

Disable a device:

```bash
xinput float <DEVICE_ID>
```

Reattach a device:

```bash
xinput reattach <DEVICE_ID> <MASTER_ID>
```

## Safer Python Experiment

Use:

```text
scripts/python/keyboard_lock_x11_experiment.py
```

The script is intentionally conservative and prints the detected devices before acting.

## Recovery

If input is blocked accidentally:

- Use SSH from another machine.
- Reboot the host.
- Restart the display manager.
- Reattach the device manually with `xinput`.

## Notes

For kiosk-style systems, prefer dedicated kiosk/session configuration instead of runtime keyboard detachment.
