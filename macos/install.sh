#!/usr/bin/env bash
# Install the Piercing layout on macOS for the current user:
#  1. piercing.keylayout -> ~/Library/Keyboard Layouts (the layout itself)
#  2. hidutil LaunchAgent  (Caps->Backspace, Backspace->Forward Delete)
#  3. Karabiner rule       (AltGr vim arrows; optional, needs Karabiner-Elements)
set -euo pipefail

[[ "$(uname)" == "Darwin" ]] || { echo "ERROR: run this on macOS." >&2; exit 1; }

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$HOME/Library/Keyboard Layouts"
install -m 644 "$SRC/piercing.keylayout" "$HOME/Library/Keyboard Layouts/"
echo "Installed layout -> ~/Library/Keyboard Layouts/piercing.keylayout"

mkdir -p "$HOME/Library/LaunchAgents"
install -m 644 "$SRC/com.piercingxx.keyremap.plist" "$HOME/Library/LaunchAgents/"
launchctl unload "$HOME/Library/LaunchAgents/com.piercingxx.keyremap.plist" 2>/dev/null || true
launchctl load "$HOME/Library/LaunchAgents/com.piercingxx.keyremap.plist"
echo "Installed remaps  -> Caps=Backspace, Backspace=Delete (applied now + at login)"

KARABINER_DIR="$HOME/.config/karabiner/assets/complex_modifications"
if [[ -d "$HOME/.config/karabiner" ]] || command -v karabiner_cli >/dev/null 2>&1; then
    mkdir -p "$KARABINER_DIR"
    install -m 644 "$SRC/karabiner-piercing-arrows.json" "$KARABINER_DIR/"
    echo "Installed Karabiner rule — enable it under Karabiner-Elements ->"
    echo "  Complex Modifications -> Add rule -> 'Piercing AltGr arrows'."
else
    echo "Karabiner-Elements not found — skipped the AltGr-arrows rule."
    echo "  (brew install --cask karabiner-elements, then re-run this script.)"
fi

cat <<'EOF'

Select the layout: System Settings -> Keyboard -> Text Input -> Input
Sources -> Edit -> + -> Others -> Piercing. Log out/in if it doesn't
appear immediately.

Roll back: remove the input source, then
  launchctl unload ~/Library/LaunchAgents/com.piercingxx.keyremap.plist
  rm ~/Library/LaunchAgents/com.piercingxx.keyremap.plist
  hidutil property --set '{"UserKeyMapping":[]}'
  rm "~/Library/Keyboard Layouts/piercing.keylayout"
EOF
