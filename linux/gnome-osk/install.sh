#!/usr/bin/env bash
# Install the Piercing GNOME Shell OSK layout as a user extension.
#
# The extension registers an extra gresource containing piercing.json at
# runtime, so the on-screen keyboard finds a layout for the 'piercing'
# input source. Unlike patching the system bundle (install-system.sh),
# this is user-level, needs no sudo, and survives gnome-shell updates.
#
# The xkb layout must be installed and selected first (../install.sh) —
# the OSK only shows piercing.json while 'piercing' is the active source.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UUID="piercing-osk@piercingxx.github.io"
DEST="${XDG_DATA_HOME:-$HOME/.local/share}/gnome-shell/extensions/$UUID"

command -v glib-compile-resources >/dev/null || {
    echo "ERROR: glib-compile-resources not found (package: glib2 / libglib2.0-dev-bin)." >&2
    exit 1
}

workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

cp "$SRC/piercing.json" "$workdir/piercing.json"
cat > "$workdir/piercing-osk.gresource.xml" <<'XML'
<?xml version="1.0" encoding="UTF-8"?>
<gresources>
  <gresource prefix="/org/gnome/shell/osk-layouts">
    <file>piercing.json</file>
  </gresource>
</gresources>
XML
glib-compile-resources --sourcedir="$workdir" \
    --target="$workdir/piercing-osk.gresource" "$workdir/piercing-osk.gresource.xml"

mkdir -p "$DEST"
install -m 644 "$SRC/extension/extension.js" "$SRC/extension/metadata.json" \
    "$workdir/piercing-osk.gresource" "$DEST/"
echo "Installed extension -> $DEST"

if command -v gnome-extensions >/dev/null; then
    gnome-extensions enable "$UUID" 2>/dev/null \
        && echo "Extension enabled." \
        || echo "Enable it after re-login with: gnome-extensions enable $UUID"
else
    echo "Enable it after re-login with: gnome-extensions enable $UUID"
fi

cat <<'EOF'

Log out and back in so gnome-shell picks up the new extension, then the
OSK shows the Piercing layout whenever "English (Piercing)" is active.

Remove with:  gnome-extensions uninstall piercing-osk@piercingxx.github.io
EOF
