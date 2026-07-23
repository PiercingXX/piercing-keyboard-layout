#!/usr/bin/env python3
"""PiercingXX 4x12 keymap tool (sporewoh minipeg48, Vial firmware).

Reads/writes the dynamic keymap over VIA/Vial raw HID. The firmware keeps
sending STANDARD key positions — the OS Piercing layout does the letter
remapping. This tool only rearranges layers/thumb keys to match the
Piercing workflow.

Usage:
  ./apply-piercing.py              # dry run: show what would change
  ./apply-piercing.py --apply      # write the Piercing keymap to the board
  ./apply-piercing.py --dump out.bin
  ./apply-piercing.py --restore minipeg48-keymap-backup-2026-07-22.bin

The board keymap is stored in its EEPROM — applying is instant, no reflash,
and Vial will show the new map. Always restorable from the backup .bin.

The minipeg48 matrix is a plain 4x12 grid, so the visual layout below maps
straight onto it (no Preonic-style bottom-row shuffle).

BOTTOM ROW: the board is built 2x2u, so only one switch is wired under each
2u cap while the matrix still exposes 12 slots. Which half of a pair is live
isn't discoverable over HID, so the bottom row keeps the slot assignment
that is already proven working on this board — Enter on slots 4/5/6 and
Space on slot 7 — rather than a tidier 4,5=Enter / 6,7=Space split that
would silently kill Enter if slot 6 turned out to be the live one.
"""
import argparse, glob, os, select, struct, sys

ROWS, COLS, LAYERS = 4, 12, 6
TOTAL = LAYERS * ROWS * COLS * 2
HID_NAME = "minipeg48"

# ---------------------------------------------------------------- keycodes
TRNS, NO = 0x0001, 0x0000
def S(kc): return 0x0200 | kc            # shifted
def LT(layer, kc): return 0x4000 | (layer << 8) | kc
K = dict(A=0x04,B=0x05,C=0x06,D=0x07,E=0x08,F=0x09,G=0x0A,H=0x0B,I=0x0C,J=0x0D,
K=0x0E,L=0x0F,M=0x10,N=0x11,O=0x12,P=0x13,Q=0x14,R=0x15,S=0x16,T=0x17,U=0x18,
V=0x19,W=0x1A,X=0x1B,Y=0x1C,Z=0x1D,N1=0x1E,N2=0x1F,N3=0x20,N4=0x21,N5=0x22,
N6=0x23,N7=0x24,N8=0x25,N9=0x26,N0=0x27,ENT=0x28,ESC=0x29,BSPC=0x2A,TAB=0x2B,
SPC=0x2C,MINS=0x2D,EQL=0x2E,LBRC=0x2F,RBRC=0x30,BSLS=0x31,SCLN=0x33,QUOT=0x34,
CAPS=0x39,GRV=0x35,COMM=0x36,DOT=0x37,SLSH=0x38,F1=0x3A,F2=0x3B,F3=0x3C,F4=0x3D,F5=0x3E,
F6=0x3F,F7=0x40,F8=0x41,F9=0x42,F10=0x43,F11=0x44,F12=0x45,PSCR=0x46,INS=0x49,
DEL=0x4C,RGHT=0x4F,LEFT=0x50,DOWN=0x51,UP=0x52,PSLS=0x54,PAST=0x55,
PMNS=0x56,PPLS=0x57,PDOT=0x63,VOLU=0xA9,VOLD=0xAA,MPLY=0xAE,
LCTL=0xE0,LSFT=0xE1,LALT=0xE2,LGUI=0xE3,RSFT=0xE5,RALT=0xE6)

# Digits re-encoded for the Piercing OS layout (digits live on Shift, in
# alternating-hand order), so the numpad layer still types real digits:
# digit -> Shift + (physical number key whose shifted value is that digit)
DIG = {1:S(K['N5']),2:S(K['N7']),3:S(K['N4']),4:S(K['N8']),5:S(K['N3']),
       6:S(K['N9']),7:S(K['N2']),8:S(K['N0']),9:S(K['N1']),0:S(K['N6'])}

# --------------------------------------------------- visual layers (4x12)
k = K
L0 = [  # base — standard positions; OS layout renders Piercing
 [k['TAB'],k['Q'],k['W'],k['E'],k['R'],k['T'],k['Y'],k['U'],k['I'],k['O'],k['P'],k['DEL']],
 [k['CAPS'],k['A'],k['S'],k['D'],k['F'],k['G'],k['H'],k['J'],k['K'],k['L'],k['SCLN'],k['QUOT']],
 [k['LSFT'],LT(1,k['Z']),LT(2,k['X']),LT(3,k['C']),k['V'],k['B'],k['N'],k['M'],k['COMM'],k['DOT'],k['SLSH'],k['RSFT']],
 [k['LCTL'],k['LGUI'],k['LALT'],k['RALT'],k['ENT'],k['ENT'],k['ENT'],k['SPC'],k['PSCR'],k['VOLD'],k['VOLU'],k['ESC']],
]
# Layer 1 arrows sit on the keys that TYPE h/j/k/l under Piercing (vim-style,
# arrows follow the letters): h=Left (home row), j=Down (bottom, old . spot),
# k=Up (bottom, old N spot), l=Right (top row, old U spot).
L1 = [  # hold the ,-key (tap = comma): vim arrows, symbol column
 [TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,NO,k['RGHT'],NO,NO,k['MINS'],k['EQL']],
 [TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,k['LEFT'],NO,NO,NO,k['BSLS'],k['GRV']],
 [TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,k['UP'],NO,NO,k['DOWN'],k['LBRC'],k['RBRC']],
 [TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,k['MPLY'],TRNS,TRNS,TRNS],
]
L2 = [  # hold the c-key (tap = c): numpad (Piercing-safe digits)
 [TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,k['PPLS'],DIG[7],DIG[8],DIG[9],k['MINS'],k['EQL']],
 [TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,k['PMNS'],DIG[4],DIG[5],DIG[6],k['BSLS'],k['GRV']],
 [TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,k['PDOT'],DIG[1],DIG[2],DIG[3],k['LBRC'],k['RBRC']],
 [TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,DIG[0],k['PDOT'],TRNS,TRNS,TRNS],
]
L3 = [  # hold the x-key (tap = x): the number row + F-row this board lacks
 [k['GRV'],k['N1'],k['N2'],k['N3'],k['N4'],k['N5'],k['N6'],k['N7'],k['N8'],k['N9'],k['N0'],k['DEL']],
 [k['F12'],k['F1'],k['F2'],k['F3'],k['F4'],k['F5'],k['F6'],k['F7'],k['F8'],k['F9'],k['F10'],k['INS']],
 [TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,NO,NO,NO,NO,NO,TRNS],
 [TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS,TRNS],
]
L4 = [[TRNS]*12 for _ in range(4)]
L5 = [[TRNS]*12 for _ in range(4)]

def build_buffer():
    out = b""
    for layer in (L0, L1, L2, L3, L4, L5):
        for row in layer:
            out += struct.pack(">12H", *row)
    assert len(out) == TOTAL
    return out

# ------------------------------------------------------------------- HID
def find_device():
    for path in sorted(glob.glob("/sys/class/hidraw/hidraw*")):
        try:
            uevent = open(f"{path}/device/uevent").read()
            rdesc = open(f"{path}/device/report_descriptor", "rb").read()
        except OSError:
            continue
        if HID_NAME in uevent and b"\x06\x60\xff" in rdesc:
            return "/dev/" + os.path.basename(path)
    sys.exit(f"{HID_NAME} raw-HID interface not found — is the board plugged in?")

class Board:
    def __init__(self, dev): self.fd = os.open(dev, os.O_RDWR)
    def xfer(self, payload):
        os.write(self.fd, bytes([0]) + payload + bytes(32 - len(payload)))
        r,_,_ = select.select([self.fd], [], [], 1.0)
        if not r: raise TimeoutError("keyboard did not respond")
        return os.read(self.fd, 32)
    def read_keymap(self):
        data, off = b"", 0
        while off < TOTAL:
            n = min(28, TOTAL - off)
            data += self.xfer(bytes([0x12]) + struct.pack(">H", off) + bytes([n]))[4:4+n]
            off += n
        return data
    def write_keymap(self, data):
        assert len(data) == TOTAL
        off = 0
        while off < TOTAL:
            n = min(28, TOTAL - off)
            self.xfer(bytes([0x13]) + struct.pack(">H", off) + bytes([n]) + data[off:off+n])
            off += n

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write Piercing keymap to the board")
    ap.add_argument("--restore", metavar="BACKUP.bin", help="write a saved keymap back")
    ap.add_argument("--dump", metavar="OUT.bin", help="save current board keymap and exit")
    args = ap.parse_args()

    board = Board(find_device())
    current = board.read_keymap()

    if args.dump:
        open(args.dump, "wb").write(current); print(f"saved -> {args.dump}"); return

    target = open(args.restore, "rb").read() if args.restore else build_buffer()
    if args.restore and len(target) != TOTAL:
        sys.exit(f"{args.restore}: expected {TOTAL} bytes, got {len(target)}")

    cur = struct.unpack(f">{TOTAL//2}H", current)
    new = struct.unpack(f">{TOTAL//2}H", target)
    diffs = [(i, c, n) for i, (c, n) in enumerate(zip(cur, new)) if c != n]
    print(f"{len(diffs)} key slots differ from what's on the board.")
    for i, c, n in diffs:
        layer, rest = divmod(i, ROWS*COLS); row, col = divmod(rest, COLS)
        print(f"  L{layer} matrix[{row}][{col}]: {c:#06x} -> {n:#06x}")

    if not (args.apply or args.restore):
        print("\nDry run only. Use --apply to write (or --restore <backup>).")
        return
    if not diffs:
        print("Nothing to do."); return
    board.write_keymap(target)
    verify = board.read_keymap()
    print("verified OK — board now matches." if verify == target
          else "WARNING: verify mismatch — re-run, or restore from backup.")

if __name__ == "__main__":
    main()
