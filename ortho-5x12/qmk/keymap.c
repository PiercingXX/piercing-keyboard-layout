// PiercingXX 5x12 ortholinear keymap (Drop Preonic rev3, LAYOUT_preonic_2x2uC)
// Bottom row: 4 keys | 2u Enter | 2u Space | 4 keys
//
// This is the SOURCE-CODE MIRROR of the live Vial keymap that
// preonic-vial/apply-piercing.py writes. You normally don't need to compile
// this — it exists so the layout survives even without the Vial EEPROM.
//
// ARCHITECTURE: firmware sends STANDARD US-position scancodes; the Piercing
// remap lives in the OS layout (xkb / Windows .klc / Android .kcm). Do not
// bake the letter remap into firmware or it will double-remap.
//
// Because the OS layout swaps things around, keys are named here by their
// PHYSICAL position; the comments show what the OS actually renders.
//
// Rendered base layer:
//   `~  !9  @7  #5  $3  %1  ^0  &2  *4  (6  )8  Del
//   Tab  q   r   f   w   g   ;:  l   p   y   z   Play
//   Bksp a   s   e   t   d   h   n   u   i   o   '"
//   Shft ,(hold L1) c(hold L2) x  v  /?  k  m  b  j  .>  Shft
//   Ctrl Super Alt AltGr [ Enter ] [ Space ] PrtSc Vol- Vol+ Esc
//
// Layer 1 (hold the ,-key or press AltGr thumb + letter for OS arrows):
//   F12 F1-F10 Ins / arrows on the keys that TYPE h,j,k,l (vim: arrows
//   follow the letters) / - = \ ` [ ]
// Layer 2 (hold the c-key): numpad. Digits are encoded as Shift+number-
//   position so they still type real digits under the Piercing OS layout.

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
    [0] = LAYOUT_preonic_2x2uC(
        KC_GRV,  KC_1,         KC_2,         KC_3,    KC_4,    KC_5,    KC_6,    KC_7,    KC_8,    KC_9,    KC_0,    KC_DEL,
        KC_TAB,  KC_Q,         KC_W,         KC_E,    KC_R,    KC_T,    KC_Y,    KC_U,    KC_I,    KC_O,    KC_P,    KC_MPLY,
        KC_CAPS, KC_A,         KC_S,         KC_D,    KC_F,    KC_G,    KC_H,    KC_J,    KC_K,    KC_L,    KC_SCLN, KC_QUOT,
        KC_LSFT, LT(1, KC_Z),  LT(2, KC_X),  KC_C,    KC_V,    KC_B,    KC_N,    KC_M,    KC_COMM, KC_DOT,  KC_SLSH, KC_RSFT,
        KC_LCTL, KC_LGUI,      KC_LALT,      KC_RALT,      KC_ENT,           KC_SPC,      KC_PSCR, KC_VOLD, KC_VOLU, KC_ESC
    ),
    // arrows: LEFT on the h-key (QWERTY H pos), RIGHT on the l-key (QWERTY U
    // pos), UP on the k-key (QWERTY N pos), DOWN on the j-key (QWERTY . pos)
    [1] = LAYOUT_preonic_2x2uC(
        KC_F12,  KC_F1,   KC_F2,   KC_F3,   KC_F4,   KC_F5,   KC_F6,   KC_F7,   KC_F8,   KC_F9,   KC_F10,  KC_INS,
        _______, _______, _______, _______, _______, _______, XXXXXXX, KC_RGHT, XXXXXXX, XXXXXXX, KC_MINS, KC_EQL,
        _______, _______, _______, _______, _______, _______, KC_LEFT, XXXXXXX, XXXXXXX, XXXXXXX, KC_BSLS, KC_GRV,
        _______, _______, _______, _______, _______, _______, KC_UP,   XXXXXXX, XXXXXXX, KC_DOWN, KC_LBRC, KC_RBRC,
        _______, _______, _______, _______,      _______,          _______,     KC_MPLY, _______, _______, _______
    ),
    [2] = LAYOUT_preonic_2x2uC(
        _______, _______, _______, _______, _______, _______, _______, KC_NUM,  KC_PSLS, KC_PAST, KC_PMNS, KC_INS,
        _______, _______, _______, _______, _______, _______, KC_PPLS, PD_7,    PD_8,    PD_9,    KC_MINS, KC_EQL,
        _______, _______, _______, _______, _______, _______, KC_PMNS, PD_4,    PD_5,    PD_6,    KC_BSLS, KC_GRV,
        _______, _______, _______, _______, _______, _______, KC_PDOT, PD_1,    PD_2,    PD_3,    KC_LBRC, KC_RBRC,
        _______, _______, _______, _______,      _______,          PD_0,        KC_PDOT, _______, _______, _______
    ),
    [3] = LAYOUT_preonic_2x2uC(
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______,      _______,          _______,     _______, _______, _______, _______
    )
};
