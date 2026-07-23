// PiercingXX Charybdis 3x6 keymap (BastardKB charybdis/3x6, 41 keys)
//
// This is the SOURCE-CODE MIRROR of the live Vial keymap that
// ../piercing-charybdis-3x6.layout.json imports. You normally don't need
// to compile this — it exists so the layout survives even without the
// Vial EEPROM.
//
// ARCHITECTURE: firmware sends STANDARD US-position scancodes; the
// Piercing remap lives in the OS layout (xkb / Windows .klc / Android
// .kcm). Do not bake the letter remap into firmware or it will
// double-remap. Keys are named here by their PHYSICAL position; the
// comments show what the OS actually renders.
//
// The 3x6 letter block is exactly the lower three rows of the Planck
// layout, so those carry over unchanged. Only the thumbs differ: this
// board has 5 (3 left + 2 right) where the Planck bottom row has 10
// functions, so AltGr, PrtSc, Vol-, Vol+ and Play live on layer 3.
//
// Rendered base layer:
//   Tab  q    r    f    w   g  |  ;:  l   p   y   z   Del
//   Bksp a    s    e    t   d  |  h   n   u   i   o   '"
//   Shft ,L1  cL2  xL3  v   /? |  k   m   b   j   .>  Esc
//              Ctrl Super Enter | Space Alt
//
// Layer 1 (hold the ,-key): vim arrows on the keys that TYPE h/j/k/l
//   (arrows follow the letters), - = \ ` [ ] symbol column
// Layer 2 (hold the c-key): numpad. Digits are encoded as Shift+number-
//   position so they still type real digits under the Piercing OS layout.
// Layer 3 (hold the x-key): everything a 41-key board has no room for —
//   the number row, the F-row, Del/Ins, the media/PrtSc thumbs, and the
//   trackball block (sniping, drag-scroll, DPI, mouse buttons).

#include QMK_KEYBOARD_H

// digit -> Shift + (number key whose shifted value is that digit)
#define PD_1 S(KC_5)
#define PD_2 S(KC_7)
#define PD_3 S(KC_4)
#define PD_4 S(KC_8)
#define PD_5 S(KC_3)
#define PD_6 S(KC_9)
#define PD_7 S(KC_2)
#define PD_8 S(KC_0)
#define PD_9 S(KC_1)
#define PD_0 S(KC_6)

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [0] = LAYOUT(
        KC_TAB,  KC_Q,         KC_W,         KC_E,         KC_R,    KC_T,       KC_Y,    KC_U,    KC_I,    KC_O,    KC_P,    KC_DEL,
        KC_CAPS, KC_A,         KC_S,         KC_D,         KC_F,    KC_G,       KC_H,    KC_J,    KC_K,    KC_L,    KC_SCLN, KC_QUOT,
        KC_LSFT, LT(1, KC_Z),  LT(2, KC_X),  LT(3, KC_C),  KC_V,    KC_B,       KC_N,    KC_M,    KC_COMM, KC_DOT,  KC_SLSH, KC_ESC,
                             KC_LCTL, KC_LGUI, KC_ENT,             KC_SPC,  KC_LALT
    ),
    // arrows: LEFT on the h-key (QWERTY H pos), RIGHT on the l-key (QWERTY U
    // pos), UP on the k-key (QWERTY N pos), DOWN on the j-key (QWERTY . pos)
    [1] = LAYOUT(
        _______, _______, _______, _______, _______, _______,   XXXXXXX, KC_RGHT, XXXXXXX, XXXXXXX, KC_MINS, KC_EQL,
        _______, _______, _______, _______, _______, _______,   KC_LEFT, XXXXXXX, XXXXXXX, XXXXXXX, KC_BSLS, KC_GRV,
        _______, _______, _______, _______, _______, _______,   KC_UP,   XXXXXXX, XXXXXXX, KC_DOWN, KC_LBRC, KC_RBRC,
                          _______, _______, _______,          _______, KC_RALT
    ),
    [2] = LAYOUT(
        _______, _______, _______, _______, _______, _______,   KC_PPLS, PD_7,    PD_8,    PD_9,    KC_MINS, KC_EQL,
        _______, _______, _______, _______, _______, _______,   KC_PMNS, PD_4,    PD_5,    PD_6,    KC_BSLS, KC_GRV,
        _______, _______, _______, _______, _______, _______,   KC_PDOT, PD_1,    PD_2,    PD_3,    KC_LBRC, KC_RBRC,
                          _______, _______, _______,          PD_0,    KC_PDOT
    ),
    [3] = LAYOUT(
        KC_GRV,  KC_1,    KC_2,    KC_3,    KC_4,    KC_5,      KC_6,    KC_7,        KC_8,        KC_9,        KC_0,    KC_DEL,
        KC_F12,  KC_F1,   KC_F2,   KC_F3,   KC_F4,   KC_F5,     KC_F6,   KC_F7,       KC_F8,       KC_F9,       KC_F10,  KC_INS,
        _______, _______, _______, _______, DPI_MOD, S_D_MOD,   SNIPING, KC_MS_BTN1,  KC_MS_BTN3,  KC_MS_BTN2,  DRGSCRL, _______,
                          KC_PSCR, KC_VOLD, KC_VOLU,          KC_MPLY, KC_RALT
    )
};
