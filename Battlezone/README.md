# Battlezone — Piercing config

Battlezone binds keys by **character**, not by scancode. That is why a
`Colemak/` variant has to exist at all: change the OS layout and every
letter binding moves to a different physical key. `Piercing/` is the same
config carried over the same way.

The rule, taken from how `Colemak/` was derived from `Qwerty/`, is a
**positional remap** — every action keeps its physical key, and the
binding is rewritten to whatever character that key produces under the
new layout:

| Physical key (QWERTY label) | Qwerty | Colemak | Piercing |
|---|---|---|---|
| W | W | W | **R** |
| E | E | F | **F** |
| R | R | P | **W** |
| T | T | G | **G** |
| I | I | I | **P** |
| P | P | K¹ | **Z** |
| S | S | R | **S** |
| D | D | S | **E** |
| F | F | T | **T** |
| G | G | D | **D** |
| Z | Z | Z | **Comma** |
| X | X | X | **C** |
| C | C | C | **X** |
| B | B | B | **Slash** |
| N | N | N | **K** |
| `,` | Comma | Comma | **B** |

Everything else — digits, `-`/`=`, F-keys, arrows, the Grey\* keypad
block, Space/Tab/Insert and the modifiers — sits on a position Piercing
doesn't move, so it passes through untouched.

Regenerate with `./build-piercing.py` (run from this directory). It
rewrites `input.map` and `SBPPrefs.txt` from the `Qwerty/` baseline and
copies `gamekey.map` and the voice-pack `.wav` files unchanged.
`gamekey.map` is byte-identical across all three variants.

## Verified

All 119 keyboard bindings convert, every one matching the positional
rule. A positional remap is a bijection, so no new key collisions are
introduced — the 24 keys that serve more than one action (different
program modes) are the same 24 before and after. CRLF line endings are
preserved byte-for-byte in all three text files, which matters because
the game parses them on Windows.

## Two things to check in-game

1. **`eject` now sits on `Slash`.** That key name does not appear
   anywhere in the stock files, so it is the one binding whose name this
   repo cannot confirm the game accepts. If eject is dead, rebind it in
   game and the correct spelling will be written back to `input.map`.
2. **The number row is left alone.** Under Piercing those keys produce
   symbols unshifted (`!` `@` `#` …) with digits on Shift, so
   `mode_select_1`–`9` may not fire. Colemak's number row is identical to
   QWERTY's, so the existing variants give no evidence either way. If the
   mode-select keys misbehave, that is the cause.

¹ Colemak's `pitch_down` is the one binding that breaks the positional
rule — the physical P key produces `;` under Colemak, not `K`. It looks
like a hand-picked substitution. Piercing follows the positional rule
here (`Z`); change it if you preferred whatever motivated that choice.
