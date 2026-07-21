#!/usr/bin/env bash
# Install the Piercing keyd config (system-wide evdev remap: GDM, TTYs,
# every compositor, all users). Needs sudo; keyd must be installed
# (pacman -S keyd / apt install keyd) and its service enabled.
#
# WARNING: this replaces the xkb approach. After installing, set your
# session's input source back to plain "English (US)" — keyd + the
# piercing xkb layout together remap letters twice.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONF="/etc/keyd/default.conf"

command -v keyd >/dev/null || {
    echo "ERROR: keyd not installed (package: keyd)." >&2
    exit 1
}

if [[ -e "$CONF" ]] && ! cmp -s "$SRC/piercing.conf" "$CONF"; then
    sudo cp -f "$CONF" "$CONF.orig"
    echo "Backed up existing config -> $CONF.orig"
fi

sudo mkdir -p /etc/keyd
sudo install -m 644 "$SRC/piercing.conf" "$CONF"
sudo systemctl enable --now keyd >/dev/null 2>&1 || true
sudo keyd reload
echo "Installed $CONF and reloaded keyd."

cat <<'EOF'

Now set your session input source to plain "English (US)" (remove the
piercing xkb source) — keyd already does the remapping underneath.

Check it's live:    sudo keyd monitor      (type and watch translated keys)
Restore stock:      sudo rm /etc/keyd/default.conf && sudo keyd reload
                    (or put back /etc/keyd/default.conf.orig)
EOF
