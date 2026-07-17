#!/usr/bin/env bash
# Install the PiercingXX layout for the current user (X11 and Wayland).
# This only makes "piercing" AVAILABLE to select — it does NOT activate it.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
XKB_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/xkb"

mkdir -p "$XKB_DIR/symbols" "$XKB_DIR/rules"
install -m 644 "$SRC/xkb/symbols/piercing" "$XKB_DIR/symbols/piercing"
echo "Installed symbols -> $XKB_DIR/symbols/piercing"

RULES="$XKB_DIR/rules/evdev.xml"
if [[ ! -e "$RULES" ]]; then
    install -m 644 "$SRC/xkb/rules/evdev.xml" "$RULES"
    echo "Installed rules   -> $RULES"
elif grep -q "<name>piercing</name>" "$RULES"; then
    echo "Already registered in $RULES"
else
    echo "NOTE: $RULES already exists and doesn't mention piercing."
    echo "Add this block inside its <layoutList>:"
    sed -n '/<layout>/,/<\/layout>/p' "$SRC/xkb/rules/evdev.xml"
fi

echo
if command -v xkbcli >/dev/null; then
    if xkbcli compile-keymap --layout piercing >/dev/null 2>&1; then
        echo "Verified: layout compiles cleanly (libxkbcommon / Wayland path)."
    else
        echo "WARNING: xkbcli failed to compile the layout:" >&2
        xkbcli compile-keymap --layout piercing >/dev/null || true
    fi
fi

cat <<'EOF'

To switch to it later:
  GNOME/KDE (Wayland):  add "English (Piercing)" as an input source in
                        keyboard settings (log out/in first so it appears)
  sway:                 input type:keyboard xkb_layout piercing
  Hyprland:             input { kb_layout = piercing }
  X11 session:          setxkbmap -I$HOME/.config/xkb piercing -print \
                          | xkbcomp -I$HOME/.config/xkb - $DISPLAY
EOF
