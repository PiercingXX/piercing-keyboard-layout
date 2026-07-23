#!/usr/bin/env python3
"""Generate the Piercing Battlezone config from the QWERTY baseline.

Battlezone binds by CHARACTER, not scancode — that is why a Colemak
variant has to exist at all. So porting to Piercing is a positional
remap: every action keeps its PHYSICAL key, and the binding is rewritten
to whatever character that physical key produces under Piercing.

The Colemak/ folder is the worked example of the same transformation
(QWERTY S position -> "R", D -> "S", E -> "F", ...), and this script
applies the identical rule with the Piercing table instead.

Run from the Battlezone/ directory:  ./build-piercing.py
"""
import pathlib, re, shutil, sys

SRC = pathlib.Path("Qwerty")
DST = pathlib.Path("Piercing")

# QWERTY physical position -> character Piercing produces there.
#   row1  q r f w g ;  l p y z      (QWERTY Q W E R T Y U I O P)
#   row2  a s e t d h  n u i o      (QWERTY A S D F G H J K L ;)
#   row3  , c x v / k  m b j .      (QWERTY Z X C V B N M , . /)
POS = {
    "Q": "Q", "W": "R", "E": "F", "R": "W", "T": "G",
    "Y": "Semicolon", "U": "L", "I": "P", "O": "Y", "P": "Z",
    "A": "A", "S": "S", "D": "E", "F": "T", "G": "D",
    "H": "H", "J": "N", "K": "U", "L": "I", "Semicolon": "O",
    "Z": "Comma", "X": "C", "C": "X", "V": "V", "B": "Slash",
    "N": "K", "M": "M", "Comma": "B", "Period": "J", "Slash": "Period",
}
# Everything else — digits, Minus/Equal, F-keys, arrows, Grey* keypad,
# Space/Tab/Insert, and the modifiers — sits on a position Piercing does
# not move, so it passes through untouched.


def remap(token):
    """Rewrite one key name, preserving the source's letter case."""
    hit = POS.get(token.capitalize() if len(token) > 1 else token.upper())
    if hit is None:
        return token
    # keep a lowercase source lowercase, but only when the result is also a
    # single letter — named keys like Comma stay properly capitalised
    if len(token) == 1 and token.islower() and len(hit) == 1:
        return hit.lower()
    return hit


def convert_input_map(text):
    def sub(m):
        return m.group(1) + remap(m.group(2))
    return re.sub(r"^([ \t]*[+-][ \t]*keyboard[ \t]+)(\S+)", sub, text, flags=re.M)


# SBPPrefs settings whose value is a key name. Values may carry a
# "Shift+"/"Ctrl+" prefix, or be the literal "unassigned".
KEY_SETTINGS = re.compile(
    r"^([ \t]*(?:TargetHotkey|RemoteTargetHotkey|AreaSelectHotkey|AutoLevelToggle"
    r"|FireCannonHotkey|FireRocketHotkey|FireMortarHotkey|FireSpecialHotkey"
    r"|SetManualHotkey|JetPack\w+Key)[ \t]*=[ \t]*)([^\r\n]+?)([ \t]*\r?)$",
    re.M | re.I,
)   # the trailing \r is captured, not consumed — these files must stay CRLF


def convert_prefs(text):
    def sub(m):
        head, value, tail = m.group(1), m.group(2), m.group(3)
        if value.strip().lower() in ("unassigned", ""):
            return m.group(0)
        *mods, key = value.strip().split("+")
        return head + "+".join(mods + [remap(key)]) + tail
    return KEY_SETTINGS.sub(sub, text)


def main():
    if not SRC.is_dir():
        sys.exit("run this from the Battlezone/ directory (no Qwerty/ here)")
    DST.mkdir(exist_ok=True)
    for f in sorted(SRC.iterdir()):
        # newline="" keeps the game's CRLF line endings byte-for-byte
        if f.name == "input.map":
            text = f.read_text(encoding="utf-8", errors="surrogateescape", newline="")
            (DST / f.name).write_text(convert_input_map(text), encoding="utf-8",
                                      errors="surrogateescape", newline="")
        elif f.name == "SBPPrefs.txt":
            text = f.read_text(encoding="utf-8", errors="surrogateescape", newline="")
            (DST / f.name).write_text(convert_prefs(text), encoding="utf-8",
                                      errors="surrogateescape", newline="")
        else:
            shutil.copy2(f, DST / f.name)   # gamekey.map + the .wav voice packs
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
