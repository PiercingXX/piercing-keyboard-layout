# Charybdis 3x6 — Piercing layout

BastardKB Charybdis 3x6 (41 keys, USB `A8F8:1834`) running Vial firmware.

The 3x6 letter block is *exactly* the lower three rows of the Planck
layout, so every letter, symbol and layer key sits on the same physical
position as on the Preonic, Planck, Blank Slate and minipeg48. Only the
thumbs differ: this board has 5 (3 left + 2 right) where the Planck's
bottom row has 10 functions.

```
Tab   q    r    f    w    g   |   ;:   l    p    y    z    Del
Bksp  a    s    e    t    d   |   h    n    u    i    o    '"
Shft  ,    c    x    v    /?  |   k    m    b    j    .>   Esc
       hold: L1   L2   L3
                Ctrl Super Enter | Space Alt
```

## Layers

| Hold | Layer | Contents |
|---|---|---|
| `,` key | 1 | vim arrows on the keys that TYPE h/j/k/l, `- = \ ` [ ]` symbol column, AltGr on the right thumb |
| `c` key | 2 | numpad (digits encoded to survive the Piercing number row), same symbol column |
| `x` key | 3 | number row, F-row, Del/Ins, PrtSc · Vol− · Vol+ · Play on the thumbs, and the trackball block |

Layer 3 is the "everything a 41-key board has no room for" layer. Its
letter-row right hand carries the pointer controls: sniping, mouse
buttons 1/3/2, drag-scroll, with DPI and sniping-DPI cycling on the left.

Two deliberate deviations from the larger boards, both forced by the key
count:

- **Del and Esc take the right pinky column** (where the Planck has Play
  and RShift). This matches the layout that was already on the board —
  on a 41-key board those two are worth more than a second Shift.
- **AltGr is on layer 1/3 instead of a thumb.** It only ever drove the
  OS-level vim arrows, and layer 1 provides those directly.

## Install

Import `piercing-charybdis-3x6.layout.json` in Vial
(File → Import Keymap). Instant, no reflash, fully reversible — export
your current keymap first if you want a way back.

`qmk/keymap.c` is a compile-ready mirror for non-Vial QMK builds, and
`build-layout.py` regenerates the Vial JSON from the physical-order
tables (it handles the right half's reversed matrix rows for you).
