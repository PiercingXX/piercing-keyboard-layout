#!/usr/bin/env bash
# Install the Piercing layout into the GNOME Shell on-screen keyboard (OSK)
# by patching the SYSTEM bundle. Prefer ./install.sh (user extension, no
# sudo, survives updates); use this fallback when extensions are disabled
# or unavailable.
#
# GNOME Shell loads OSK layouts from a compiled resource bundle
# (/usr/share/gnome-shell/gnome-shell-osk-layouts.gresource) keyed by xkb
# layout name. This script extracts the system bundle, adds piercing.json,
# recompiles, and replaces the bundle (keeping a .orig backup). Needs sudo
# for the final copy, and must be re-run after gnome-shell updates.
#
# The xkb layout must be installed and selected first (../install.sh) —
# the OSK only shows piercing.json while the 'piercing' input source is
# active. A gnome-shell package update restores the stock bundle: just
# re-run this script afterwards.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GRES="/usr/share/gnome-shell/gnome-shell-osk-layouts.gresource"
PREFIX="/org/gnome/shell/osk-layouts"

[[ -r "$GRES" ]] || { echo "ERROR: $GRES not found — is this a GNOME system?" >&2; exit 1; }
command -v glib-compile-resources >/dev/null || {
    echo "ERROR: glib-compile-resources not found (package: glib2 / libglib2.0-dev-bin)." >&2
    exit 1
}

workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT
mkdir -p "$workdir/osk-layouts"

# Extract every layout from the current bundle so we rebuild it complete.
if command -v gresource >/dev/null; then
    while read -r res; do
        gresource extract "$GRES" "$res" > "$workdir/osk-layouts/${res#"$PREFIX"/}"
    done < <(gresource list "$GRES")
else
    extracted=0
    python3 - "$GRES" "$PREFIX" "$workdir/osk-layouts" <<'EOF' && extracted=1
import sys
from gi.repository import Gio
gres, prefix, dest = sys.argv[1:]
res = Gio.Resource.load(gres)
for name in res.enumerate_children(f"{prefix}/", Gio.ResourceLookupFlags.NONE):
    data = res.lookup_data(f"{prefix}/{name}", Gio.ResourceLookupFlags.NONE)
    with open(f"{dest}/{name}", "wb") as f:
        f.write(data.get_data())
EOF
    if [[ $extracted -ne 1 ]]; then
        echo "ERROR: need either the 'gresource' tool or python3 with GObject" >&2
        echo "       introspection (package: python-gobject / python3-gi)." >&2
        exit 1
    fi
fi

cp "$SRC/piercing.json" "$workdir/osk-layouts/piercing.json"

# Build the resource manifest and compile.
{
    echo '<?xml version="1.0" encoding="UTF-8"?>'
    echo '<gresources>'
    echo "  <gresource prefix=\"$PREFIX\">"
    for f in "$workdir"/osk-layouts/*; do
        echo "    <file>$(basename "$f")</file>"
    done
    echo '  </gresource>'
    echo '</gresources>'
} > "$workdir/osk-layouts.gresource.xml"

glib-compile-resources --sourcedir="$workdir/osk-layouts" \
    --target="$workdir/new.gresource" "$workdir/osk-layouts.gresource.xml"

# Sanity check before touching the system file.
if command -v gresource >/dev/null; then
    gresource list "$workdir/new.gresource" | grep -qx "$PREFIX/piercing.json"
    gresource list "$workdir/new.gresource" | grep -qx "$PREFIX/us.json"
else
    python3 - "$workdir/new.gresource" "$PREFIX" <<'EOF'
import sys
from gi.repository import Gio
res = Gio.Resource.load(sys.argv[1])
names = res.enumerate_children(f"{sys.argv[2]}/", Gio.ResourceLookupFlags.NONE)
assert "piercing.json" in names and "us.json" in names, names
EOF
fi

# Keep one pristine backup: only take it if the live bundle is still stock.
if command -v gresource >/dev/null; then
    has_piercing() { gresource list "$GRES" | grep -qx "$PREFIX/piercing.json"; }
else
    has_piercing() {
        python3 - "$GRES" "$PREFIX" <<'EOF'
import sys
from gi.repository import Gio
res = Gio.Resource.load(sys.argv[1])
names = res.enumerate_children(f"{sys.argv[2]}/", Gio.ResourceLookupFlags.NONE)
sys.exit(0 if "piercing.json" in names else 1)
EOF
    }
fi
if ! has_piercing; then
    sudo cp -f "$GRES" "$GRES.orig"
    echo "Backed up stock bundle -> $GRES.orig"
fi

sudo install -m 644 "$workdir/new.gresource" "$GRES"
echo "Installed $GRES ($(basename "$SRC")/piercing.json added)"

cat <<'EOF'

Log out and back in (Wayland) for gnome-shell to reload the bundle; on an
X11 session Alt+F2, 'r', Enter works too. The OSK shows the Piercing
layout whenever the "English (Piercing)" input source is active.

Restore stock:   sudo cp /usr/share/gnome-shell/gnome-shell-osk-layouts.gresource.orig \
                         /usr/share/gnome-shell/gnome-shell-osk-layouts.gresource
After a gnome-shell package update the stock bundle returns — re-run this
script to get the layout back.
EOF
