#!/usr/bin/env bash
# Install the Piercing Squeekboard layouts (Phosh / Linux phones) for the
# current user and enable the piercing input source. Run this ON THE PHONE,
# inside the Phosh session (Terminal app), not over SSH — gsettings needs
# the session bus.
#
# The xkb layout must be installed first (it defines the 'piercing' input
# source that squeekboard keys off): run ../install.sh once before this.
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
dest="${XDG_DATA_HOME:-$HOME/.local/share}/squeekboard/keyboards"

# Copy every layout, preserving the hint subdirectories (terminal/, email/, url/).
(cd "$repo_dir" && find . -name '*.yaml' | while read -r f; do
    mkdir -p "$dest/$(dirname "$f")"
    cp -v "$f" "$dest/$f"
done)

# Add ('xkb', 'piercing') to the input sources if it isn't there already,
# without clobbering whatever else is configured.
python3 - <<'EOF'
import ast, subprocess

out = subprocess.run(
    ["gsettings", "get", "org.gnome.desktop.input-sources", "sources"],
    check=True, capture_output=True, text=True,
).stdout.strip()
if out.startswith("@a(ss) []"):
    sources = []
else:
    sources = ast.literal_eval(out)

if ("xkb", "piercing") not in sources:
    sources.append(("xkb", "piercing"))
    value = "[" + ", ".join(f"('{typ}', '{name}')" for typ, name in sources) + "]"
    subprocess.run(
        ["gsettings", "set", "org.gnome.desktop.input-sources", "sources", value],
        check=True,
    )
    print(f"Input sources set to: {value}")
else:
    print("piercing input source already enabled.")
EOF

# Phosh respawns squeekboard automatically; the new instance picks up the layout.
pkill squeekboard || true

echo "Done. If the keyboard still shows QWERTY, tap the layout switcher key on"
echo "the OSK (or Settings -> Keyboard) and pick 'English (Piercing)'."
