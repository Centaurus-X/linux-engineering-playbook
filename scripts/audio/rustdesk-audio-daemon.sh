#!/usr/bin/env bash
set -euo pipefail

LOG="$HOME/.local/state/rustdesk-audio.log"
mkdir -p "$(dirname "$LOG")"

log_message() {
    echo "[$(date '+%F %T')] $*" | tee -a "$LOG"
}

VIRT_SINK="rustdesk_sink"
VIRT_SRC="rustdesk_virtual_mic"
POLL_SECONDS="${POLL_SECONDS:-6}"
SET_VIRT_DEFAULT_SOURCE="${SET_VIRT_DEFAULT_SOURCE:-1}"
RESTORE_HW_DEFAULT_ON_CREATE="${RESTORE_HW_DEFAULT_ON_CREATE:-1}"
ENABLE_MIC_MIX="${ENABLE_MIC_MIX:-1}"

wait_audio() {
    until pactl info >/dev/null 2>&1 && pactl get-default-sink >/dev/null 2>&1; do
        sleep 1
    done
}

default_sink() {
    pactl get-default-sink 2>/dev/null || true
}

default_source() {
    pactl get-default-source 2>/dev/null || true
}

sink_exists() {
    pactl list short sinks | awk '{print $2}' | grep -Fxq "$1"
}

source_exists() {
    pactl list short sources | awk '{print $2}' | grep -Fxq "$1"
}

clean_selfloops() {
    while read -r id name args; do
        [ "$name" = "module-loopback" ] || continue

        if echo "$args" | grep -Fq "source=${VIRT_SINK}.monitor" && echo "$args" | grep -Fq "sink=${VIRT_SINK}"; then
            pactl unload-module "$id" >/dev/null || true
        fi
    done < <(pactl list short modules)
}

loop_exists() {
    pactl list short modules \
        | grep -F "module-loopback" \
        | grep -F "source=$1" \
        | grep -Fq "sink=$2"
}

make_loop() {
    local source_name="$1"
    local sink_name="$2"

    [ -z "$source_name" ] && return 0
    [ -z "$sink_name" ] && return 0

    if [ "$source_name" = "${VIRT_SINK}.monitor" ] && [ "$sink_name" = "$VIRT_SINK" ]; then
        return 0
    fi

    loop_exists "$source_name" "$sink_name" \
        || pactl load-module module-loopback "source=$source_name" "sink=$sink_name" latency_msec=120 >/dev/null \
        || true
}

remove_loop() {
    local source_name="$1"
    local sink_name="$2"

    while read -r id name args; do
        [ "$name" = "module-loopback" ] || continue

        if echo "$args" | grep -Fq "source=$source_name" && echo "$args" | grep -Fq "sink=$sink_name"; then
            pactl unload-module "$id" >/dev/null || true
        fi
    done < <(pactl list short modules)
}

ensure_stack() {
    local before
    local after

    before="$(default_sink || true)"

    if ! sink_exists "$VIRT_SINK"; then
        pactl load-module module-null-sink \
            sink_name="$VIRT_SINK" \
            sink_properties=device.description="RustDesk_Virtual_Sink" >/dev/null || true

        pactl update-sink-proplist "$VIRT_SINK" priority.session=1 >/dev/null || true
    fi

    if ! source_exists "$VIRT_SRC"; then
        pactl load-module module-remap-source \
            master="${VIRT_SINK}.monitor" \
            source_name="$VIRT_SRC" \
            source_properties=device.description="RustDesk_Virtual_Microphone" >/dev/null || true
    fi

    if [ "$RESTORE_HW_DEFAULT_ON_CREATE" -eq 1 ]; then
        after="$(default_sink || true)"
        if [ -n "$before" ] && [ "$before" != "$VIRT_SINK" ] && [ "$after" = "$VIRT_SINK" ]; then
            pactl set-default-sink "$before" >/dev/null || true
        fi
    fi

    if [ "$SET_VIRT_DEFAULT_SOURCE" -eq 1 ] && [ "$(default_source)" != "$VIRT_SRC" ]; then
        pactl set-default-source "$VIRT_SRC" >/dev/null || true
    fi
}

choose_hw_sink() {
    local current
    current="$(default_sink)"

    if [ -n "$current" ] && [ "$current" != "$VIRT_SINK" ]; then
        echo "$current"
        return 0
    fi

    pactl list short sinks | awk '{print $2}' | grep -v '^'"$VIRT_SINK"'$' | head -n1
}

log_message "starting rustdesk audio daemon"
wait_audio

while true; do
    ensure_stack
    clean_selfloops

    current_sink="$(default_sink)"
    hardware_sink="$(choose_hw_sink || true)"

    if [ "$current_sink" = "$VIRT_SINK" ]; then
        [ -n "$hardware_sink" ] && make_loop "${VIRT_SINK}.monitor" "$hardware_sink"
        [ -n "$hardware_sink" ] && remove_loop "${hardware_sink}.monitor" "$VIRT_SINK"
    else
        [ -n "$current_sink" ] && make_loop "${current_sink}.monitor" "$VIRT_SINK"
        [ -n "$current_sink" ] && remove_loop "${VIRT_SINK}.monitor" "$current_sink"
    fi

    if [ "$ENABLE_MIC_MIX" -eq 1 ]; then
        physical_source="$(pactl list short sources | awk '{print $2}' | grep -v '^'"$VIRT_SRC"'$' | head -n1 || true)"
        [ -n "$physical_source" ] && make_loop "$physical_source" "$VIRT_SINK"
    fi

    sleep "$POLL_SECONDS"
done
