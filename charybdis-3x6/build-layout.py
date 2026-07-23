#!/usr/bin/env python3
"""Build the Piercing Vial keymap for a BastardKB Charybdis 3x6 (41 keys).

The Vial file stores an 8x6 matrix (48 slots). Rows 0-2 are the left half's
three key rows, row 3 the left thumbs; rows 4-6 are the right half's key
rows STORED REVERSED (outer pinky first), row 7 the right thumbs.

We author in physical order — three 12-wide rows exactly like the Planck,
plus 5 thumbs — and let this script do the reversal.
"""
import json, os

TRNS, NO = "KC_TRNS", "KC_NO"
# digit -> Shift + (number key whose shifted value is that digit)
PD = {1:"LSFT(KC_5)",2:"LSFT(KC_7)",3:"LSFT(KC_4)",4:"LSFT(KC_8)",5:"LSFT(KC_3)",
      6:"LSFT(KC_9)",7:"LSFT(KC_2)",8:"LSFT(KC_0)",9:"LSFT(KC_1)",0:"LSFT(KC_6)"}
# charybdis_keycodes enum order (charybdis.h) -> Vial CUSTOM(n)
DPI_MOD, DPI_RMOD  = "CUSTOM(0)", "CUSTOM(1)"
S_D_MOD, S_D_RMOD  = "CUSTOM(2)", "CUSTOM(3)"
SNIPING, SNP_TOG   = "CUSTOM(4)", "CUSTOM(5)"
DRGSCRL, DRG_TOG   = "CUSTOM(6)", "CUSTOM(7)"


def layer(row0, row1, row2, thumbs):
    """physical rows (12 wide) + 5 thumbs -> flat 48-slot matrix order."""
    for r in (row0, row1, row2):
        assert len(r) == 12, len(r)
    assert len(thumbs) == 5, len(thumbs)
    lt, rt = thumbs[0:3], thumbs[3:5]          # left x=5,6,7 | right x=9,10
    m = [None] * 48
    def put(r, c, v): m[r * 6 + c] = v
    for c in range(6):                          # left halves: direct
        put(0, c, row0[c]); put(1, c, row1[c]); put(2, c, row2[c])
    for i, c in enumerate(range(5, -1, -1)):    # right halves: reversed
        put(4, c, row0[6 + i]); put(5, c, row1[6 + i]); put(6, c, row2[6 + i])
    for r in (3, 7):                             # unused thumb slots
        for c in range(6): put(r, c, NO)
    put(3, 3, lt[0]); put(3, 4, lt[1]); put(3, 1, lt[2])   # x=5, x=6, x=7
    put(7, 1, rt[0]); put(7, 3, rt[1])                     # x=9, x=10
    assert None not in m
    return m


# ------------------------------------------------------------------ base
# Rendered: Tab q r f w g | ;: l p y z Del
#           Bsp a s e t d | h  n u i o '"
#           Sft , c x v /?| k  m b j .> Esc
#           Ctrl Super Enter | Space Alt
L0 = layer(
    ["KC_TAB",  "KC_Q",       "KC_W",       "KC_E",       "KC_R", "KC_T",
     "KC_Y",    "KC_U",       "KC_I",       "KC_O",       "KC_P", "KC_DEL"],
    ["KC_CAPS", "KC_A",       "KC_S",       "KC_D",       "KC_F", "KC_G",
     "KC_H",    "KC_J",       "KC_K",       "KC_L",       "KC_SCLN", "KC_QUOT"],
    ["KC_LSFT", "LT(1,KC_Z)", "LT(2,KC_X)", "LT(3,KC_C)", "KC_V", "KC_B",
     "KC_N",    "KC_M",       "KC_COMM",    "KC_DOT",     "KC_SLSH", "KC_ESC"],
    ["KC_LCTL", "KC_LGUI", "KC_ENT",  "KC_SPC", "KC_LALT"],
)

# ---- L1: hold the ,-key — vim arrows on the keys that TYPE h/j/k/l
L1 = layer(
    [TRNS]*6 + [NO, "KC_RGHT", NO, NO, "KC_MINS", "KC_EQL"],
    [TRNS]*6 + ["KC_LEFT", NO, NO, NO, "KC_BSLS", "KC_GRV"],
    [TRNS]*6 + ["KC_UP", NO, NO, "KC_DOWN", "KC_LBRC", "KC_RBRC"],
    [TRNS, TRNS, TRNS, TRNS, "KC_RALT"],
)

# ---- L2: hold the c-key — numpad, digits encoded to survive the Piercing row
L2 = layer(
    [TRNS]*6 + ["KC_PPLS", PD[7], PD[8], PD[9], "KC_MINS", "KC_EQL"],
    [TRNS]*6 + ["KC_PMNS", PD[4], PD[5], PD[6], "KC_BSLS", "KC_GRV"],
    [TRNS]*6 + ["KC_PDOT", PD[1], PD[2], PD[3], "KC_LBRC", "KC_RBRC"],
    [TRNS, TRNS, TRNS, PD[0], "KC_PDOT"],
)

# ---- L3: hold the x-key — everything the 41-key board has no room for:
# the number row, the F-row, and the trackball/pointer block.
L3 = layer(
    ["KC_GRV", "KC_1", "KC_2", "KC_3", "KC_4", "KC_5",
     "KC_6",   "KC_7", "KC_8", "KC_9", "KC_0", "KC_DEL"],
    ["KC_F12", "KC_F1", "KC_F2", "KC_F3", "KC_F4", "KC_F5",
     "KC_F6",  "KC_F7", "KC_F8", "KC_F9", "KC_F10", "KC_INS"],
    [TRNS, TRNS, TRNS, TRNS, DPI_MOD, S_D_MOD,
     SNIPING, "KC_MS_BTN1", "KC_MS_BTN3", "KC_MS_BTN2", DRGSCRL, TRNS],
    ["KC_PSCR", "KC_VOLD", "KC_VOLU", "KC_MPLY", "KC_RALT"],
)

out = {
    "name": "Charybdis Mini",
    "vendorProductId": 2834831412,          # 0xA8F8:0x1834 — charybdis 3x6
    "macros": [""] * 16,
    "layers": [L0, L1, L2, L3],
    "encoders": [],
}
dest = "/media/Working-Storage/GitHub/piercing-keyboard-layout/charybdis-3x6/piercing-charybdis-3x6.layout.json"
os.makedirs(os.path.dirname(dest), exist_ok=True)
json.dump(out, open(dest, "w"), indent=2)
print("wrote", dest)

# ------------------------------------------------------------ sanity dump
names = {v: k for k, v in ()}
for i, L in enumerate(out["layers"]):
    print(f"--- L{i}")
    for r in range(8):
        print(f"  r{r}: " + " | ".join(L[r*6:(r+1)*6]))
