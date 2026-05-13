# RustDesk Audio Bridge on Ubuntu 24.04

## Scope

This guide creates a persistent PipeWire/PulseAudio bridge so RustDesk can capture system audio through a virtual microphone source.

## Tested Environment

| Component | Value |
|---|---|
| OS | Ubuntu 24.04 LTS |
| Audio | PipeWire with `pipewire-pulse` |
| Remote Desktop | RustDesk |

## Goal

Create:

- A virtual playback sink: `rustdesk_sink`
- A virtual microphone source: `rustdesk_virtual_mic`
- Exactly one safe loopback path
- No self-loop and no echo
- A persistent `systemd --user` service

## Prerequisites

```bash
sudo apt update
sudo apt install -y pulseaudio-utils pipewire pipewire-pulse wireplumber
```

In RustDesk on the remote host:

```text
Settings -> Security -> Permissions -> Enable audio
```

## 1. Install the Daemon Script

Use:

```text
scripts/audio/rustdesk-audio-daemon.sh
```

Install it:

```bash
mkdir -p ~/.local/bin
cp scripts/audio/rustdesk-audio-daemon.sh ~/.local/bin/rustdesk-audio-daemon.sh
chmod 755 ~/.local/bin/rustdesk-audio-daemon.sh
```

## 2. Create the systemd User Service

```bash
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/rustdesk-audio.service
```

Content:

```ini
[Unit]
Description=Persistent RustDesk audio bridge
After=pipewire.service pipewire-pulse.service wireplumber.service sound.target
Wants=pipewire.service pipewire-pulse.service wireplumber.service

[Service]
Type=simple
ExecStartPre=/bin/sh -c 'for i in $(seq 1 120); do pactl info >/dev/null 2>&1 && pactl get-default-sink >/dev/null 2>&1 && [ -S "$XDG_RUNTIME_DIR/pulse/native" ] && exit 0; sleep 1; done; exit 1'
ExecStart=%h/.local/bin/rustdesk-audio-daemon.sh
Environment=XDG_RUNTIME_DIR=%t
Restart=always
RestartSec=3
TimeoutStartSec=150

[Install]
WantedBy=default.target
```

Enable and start:

```bash
systemctl --user daemon-reload
systemctl --user enable --now rustdesk-audio.service
```

Optional for headless boot without interactive login:

```bash
sudo loginctl enable-linger "$USER"
```

## 3. Validate

```bash
systemctl --user status rustdesk-audio.service --no-pager

pactl list short sinks | grep rustdesk_sink
pactl list short sources | grep rustdesk_virtual_mic
pactl get-default-source
pactl list short modules | grep module-loopback || echo "no loopbacks"
```

Expected:

- `rustdesk_sink` exists.
- `rustdesk_virtual_mic` exists.
- Default source is `rustdesk_virtual_mic`.
- Exactly one valid loopback exists.
- No loopback from `rustdesk_sink.monitor` to `rustdesk_sink`.

## 4. Audio Test

```bash
paplay /usr/share/sounds/alsa/Front_Center.wav
```

Alternative:

```bash
pw-play /usr/share/sounds/freedesktop/stereo/bell.oga
```

## Troubleshooting

### No Audio in RustDesk Client

Check:

```bash
pactl get-default-source
pactl list short modules | grep module-loopback
systemctl --user status rustdesk-audio.service --no-pager
```

### Echo or Feedback Loop

Restart the daemon:

```bash
systemctl --user restart rustdesk-audio.service
```

Unload suspicious loopbacks:

```bash
for id in $(pactl list short modules | awk '/module-loopback/ && /rustdesk_sink/ {print $1}'); do
  pactl unload-module "$id"
done
```

### Audio Missing After Reboot

```bash
journalctl --user -u rustdesk-audio.service -n 200 --no-pager
sed -n '1,200p' ~/.local/state/rustdesk-audio.log
```

## Rollback

```bash
systemctl --user disable --now rustdesk-audio.service
rm -f ~/.config/systemd/user/rustdesk-audio.service
rm -f ~/.local/bin/rustdesk-audio-daemon.sh
systemctl --user daemon-reload
```

Optional module cleanup:

```bash
for id in $(pactl list short modules | awk '/module-null-sink|module-remap-source|module-loopback/ {print $1}'); do
  pactl unload-module "$id"
done
```
