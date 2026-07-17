; PiercingXX layout: AltGr (Right Alt) + the keys that TYPE h/j/k/l = arrows
; (vim-style: h=Left j=Down k=Up l=Right — arrows follow the letters).
; Requires AutoHotkey v2 (https://www.autohotkey.com). Put a shortcut to
; this script in shell:startup to load it at login.
; Scancodes are used, so this works regardless of the active layout:
;   h = physical QWERTY H key, j = QWERTY . key, k = QWERTY N key,
;   l = QWERTY U key (those keys type h/j/k/l under Piercing).
; {Blind} preserves Shift/Ctrl so selection and word-jumps still work.

#Requires AutoHotkey v2.0
#SingleInstance Force

RAlt & SC023::Send "{Blind}{Left}"    ; types h
RAlt & SC034::Send "{Blind}{Down}"    ; types j
RAlt & SC031::Send "{Blind}{Up}"      ; types k
RAlt & SC016::Send "{Blind}{Right}"   ; types l
