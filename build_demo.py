#!/usr/bin/env python3
"""
C64 Cracktro Demo with bouncing sprite
"""

def text_to_petscii(text):
    result = []
    for c in text:
        if c == ' ': result.append(32)
        elif 'A' <= c <= 'Z': result.append(ord(c) - 64)
        elif 'a' <= c <= 'z': result.append(ord(c) - 96)
        elif '0' <= c <= '9': result.append(ord(c))
        elif c == '!': result.append(33)
        elif c == '*': result.append(42)
        elif c == '-': result.append(45)
        elif c == '.': result.append(46)
        else: result.append(32)
    return result

# Extended note table for Last Ninja style music
SID_NOTES = {
    # Octave 2 (bass)
    'C2': (0x08, 0x93), 'D2': (0x09, 0x91), 'E2': (0x0A, 0xAD), 'F2': (0x0B, 0x48),
    'G2': (0x0C, 0x9B), 'A2': (0x0E, 0x15), 'B2': (0x0F, 0xB4),
    # Octave 3
    'C3': (0x11, 0x25), 'D3': (0x13, 0x21), 'E3': (0x15, 0x5A), 'F3': (0x16, 0x8F),
    'G3': (0x19, 0x35), 'A3': (0x1C, 0x2B), 'B3': (0x1F, 0x67),
    # Octave 4
    'C4': (0x22, 0x49), 'D4': (0x26, 0x42), 'E4': (0x2A, 0xB4), 'F4': (0x2D, 0x1E),
    'G4': (0x32, 0x6A), 'A4': (0x38, 0x56), 'B4': (0x3E, 0xCE),
    # Octave 5
    'C5': (0x44, 0x92), 'D5': (0x4C, 0x84), 'E5': (0x55, 0x68), 'F5': (0x5A, 0x3C),
    'G5': (0x64, 0xD4), 'A5': (0x70, 0xAC),
    'REST': (0x00, 0x00)
}

# Last Ninja Japanese style - 64 note patterns
# Using Japanese "In" scale (E, F, A, B, C) for haunting Eastern feel
MELODY = [
    # Part A - Sparse Japanese melody, lots of space
    'E4','REST','REST','REST','F4','REST','E4','REST',
    'REST','REST','A4','REST','REST','REST','REST','REST',
    'B4','REST','REST','REST','A4','REST','E4','REST',
    'F4','REST','E4','REST','REST','REST','REST','REST',
    # Part B - Rising tension
    'A4','REST','B4','REST','C5','REST','REST','REST',
    'B4','REST','A4','REST','E4','REST','REST','REST',
    'F4','REST','A4','REST','E4','REST','F4','REST',
    'E4','REST','REST','REST','REST','REST','REST','REST',
]

# Bass - minimal, deep, rhythmic like Last Ninja
BASS = [
    # Sparse bass with octave hits
    'E2','REST','E3','REST','E2','REST','REST','REST',
    'E2','REST','E3','REST','E2','REST','E2','E3',
    'A2','REST','A3','REST','A2','REST','REST','REST',
    'A2','REST','A3','REST','G2','REST','G3','REST',
    # Second half - building
    'E2','REST','E3','REST','E2','E2','E3','REST',
    'F2','REST','F3','REST','E2','REST','E3','REST',
    'A2','REST','A3','REST','A2','A2','A3','REST',
    'E2','E2','E3','E2','E2','E3','E2','REST',
]

# Drums - sparse, taiko-style with rim clicks
# 1=deep kick, 2=rim/snare, 3=soft tick, 0=rest
DRUMS = [
    1,0,0,3,0,0,3,0,1,0,0,3,2,0,0,0,  # Sparse taiko feel
    1,0,0,3,0,0,3,0,1,0,3,0,2,0,3,0,  # Variation
    1,0,0,0,2,0,0,0,1,0,0,3,2,0,0,3,  # Minimal
    1,0,3,0,2,0,3,0,1,0,1,0,2,0,2,0,  # Building fill
]

# Sprite data - Pulumi logo: 9 ovals in isometric cube arrangement
# The Pulumi logo is 3 rows of 3 ovals forming a cube face pattern:
#
#        ████              <- top oval (yellow)
#     ████  ████           <- row of 2 ovals
#   ████  ████  ████       <- row of 3 ovals (widest)
#     ████  ████           <- row of 2 ovals
#        ████              <- bottom oval
#
SPRITE_DATA = [
    0b00000000, 0b00000000, 0b00000000,  # Row 1
    0b00000000, 0b11100000, 0b00000000,  # Row 2        ███
    0b00000001, 0b11110000, 0b00000000,  # Row 3       █████   (top dot)
    0b00000000, 0b11100000, 0b00000000,  # Row 4        ███
    0b00000011, 0b10001110, 0b00000000,  # Row 5      ███ ███
    0b00000111, 0b11011111, 0b00000000,  # Row 6     █████████  (2 dots)
    0b00000011, 0b10001110, 0b00000000,  # Row 7      ███ ███
    0b00001110, 0b00111000, 0b11100000,  # Row 8    ███  ███  ███
    0b00011111, 0b01111101, 0b11110000,  # Row 9   █████████████████ (3 dots)
    0b00011111, 0b01111101, 0b11110000,  # Row 10  █████████████████
    0b00001110, 0b00111000, 0b11100000,  # Row 11   ███  ███  ███
    0b00001110, 0b00111000, 0b11100000,  # Row 12   ███  ███  ███
    0b00011111, 0b01111101, 0b11110000,  # Row 13  █████████████████ (3 dots)
    0b00001110, 0b00111000, 0b11100000,  # Row 14   ███  ███  ███
    0b00000011, 0b10001110, 0b00000000,  # Row 15     ███ ███
    0b00000111, 0b11011111, 0b00000000,  # Row 16    █████████  (2 dots)
    0b00000011, 0b10001110, 0b00000000,  # Row 17     ███ ███
    0b00000000, 0b11100000, 0b00000000,  # Row 18       ███
    0b00000001, 0b11110000, 0b00000000,  # Row 19      █████   (bottom dot)
    0b00000000, 0b11100000, 0b00000000,  # Row 20       ███
    0b00000000, 0b00000000, 0b00000000,  # Row 21
]

SCREEN = 0x0400
COLORRAM = 0xD800

title = "*** CLASSIC C64 DEMO ***"
cracked = "CRACKED BY"
crew = "CLAUDE CODERS"
scroll = "    WELCOME TO THE PULUMI DEMO!   GREETINGS TO ALL CLOUD ENGINEERS!   INFRASTRUCTURE AS CODE FOREVER!   MUSIC IN THE STYLE OF THE LAST NINJA BY BEN DAGLISH...   LONG LIVE THE COMMODORE 64!       "

prg = bytearray()
def lo(a): return a & 0xFF
def hi(a): return (a >> 8) & 0xFF

# Load address
prg.extend([0x01, 0x08])
# BASIC: 10 SYS 2064
prg.extend([0x0C, 0x08, 0x0A, 0x00, 0x9E, 0x32, 0x30, 0x36, 0x34, 0x00, 0x00, 0x00])
while len(prg) < 17: prg.append(0)

code = []
BASE = 0x0810

# Zero page usage:
# $FB-$FC: scroll text pointer
# $FD: scroll counter
# $FE: music index
# $FF: frame counter
# $02: sprite X lo
# $03: sprite Y
# $04: sprite X direction (0=right, 1=left)
# $05: sprite Y direction (0=down, 1=up)

# SEI
code.append(0x78)

# Clear screen
code.extend([0xA2, 0x00])
clear_start = len(code)
code.extend([0xA9, 0x20, 0x9D, 0x00, 0x04, 0x9D, 0x00, 0x05, 0x9D, 0x00, 0x06, 0x9D, 0xE8, 0x06])
code.extend([0xA9, 0x00, 0x9D, 0x00, 0xD8, 0x9D, 0x00, 0xD9, 0x9D, 0x00, 0xDA, 0x9D, 0xE8, 0xDA])
code.append(0xE8)
branch_from = len(code) + 2
offset = (clear_start - branch_from) & 0xFF
code.extend([0xD0, offset])

# Black border/bg
code.extend([0xA9, 0x00, 0x8D, 0x20, 0xD0, 0x8D, 0x21, 0xD0])

# Print text
tpet = text_to_petscii(title)
toff = 120 + (40 - len(tpet)) // 2
for i, ch in enumerate(tpet):
    code.extend([0xA9, ch, 0x8D, lo(SCREEN+toff+i), hi(SCREEN+toff+i)])
    code.extend([0xA9, 0x01, 0x8D, lo(COLORRAM+toff+i), hi(COLORRAM+toff+i)])

cpet = text_to_petscii(cracked)
coff = 280 + (40 - len(cpet)) // 2
for i, ch in enumerate(cpet):
    code.extend([0xA9, ch, 0x8D, lo(SCREEN+coff+i), hi(SCREEN+coff+i)])
    code.extend([0xA9, 0x07, 0x8D, lo(COLORRAM+coff+i), hi(COLORRAM+coff+i)])

wpet = text_to_petscii(crew)
woff = 400 + (40 - len(wpet)) // 2
for i, ch in enumerate(wpet):
    code.extend([0xA9, ch, 0x8D, lo(SCREEN+woff+i), hi(SCREEN+woff+i)])
    code.extend([0xA9, 0x02, 0x8D, lo(COLORRAM+woff+i), hi(COLORRAM+woff+i)])

# Init SID
for i in range(25):
    code.extend([0xA9, 0x00, 0x8D, lo(0xD400+i), hi(0xD400+i)])
# SID master volume
code.extend([0xA9, 0x0F, 0x8D, 0x18, 0xD4])
# Voice 1 (lead): ADSR - soft attack for flute-like Japanese shakuhachi sound
code.extend([0xA9, 0x36, 0x8D, 0x05, 0xD4])  # Attack/Decay: A=3, D=6 (soft attack)
code.extend([0xA9, 0xC7, 0x8D, 0x06, 0xD4])  # Sustain/Release: S=C, R=7
# Voice 1 pulse width (for rich sound)
code.extend([0xA9, 0x00, 0x8D, 0x02, 0xD4])  # PW lo
code.extend([0xA9, 0x08, 0x8D, 0x03, 0xD4])  # PW hi (50% duty)
# Voice 2 (bass): ADSR - punchy bass
code.extend([0xA9, 0x00, 0x8D, 0x0C, 0xD4])  # Attack/Decay: A=0, D=0
code.extend([0xA9, 0xF6, 0x8D, 0x0D, 0xD4])  # Sustain/Release: S=F, R=6
# Voice 2 pulse width
code.extend([0xA9, 0x00, 0x8D, 0x09, 0xD4])  # PW lo
code.extend([0xA9, 0x04, 0x8D, 0x0A, 0xD4])  # PW hi (25% duty - more bass)
# Voice 3 (drums): ADSR - percussive
code.extend([0xA9, 0x00, 0x8D, 0x13, 0xD4])  # Attack/Decay: A=0, D=0
code.extend([0xA9, 0x80, 0x8D, 0x14, 0xD4])  # Sustain/Release: S=8, R=0 (quick decay)

# === INIT SPRITE ===
# Set sprite pointer (sprite 0 data at $0340 = block 13)
sprite_block_idx = len(code) + 1
code.extend([0xA9, 0x00, 0x8D, 0xF8, 0x07])  # Sprite 0 pointer at $07F8

# Enable sprite 0
code.extend([0xA9, 0x01, 0x8D, 0x15, 0xD0])  # $D015 = sprite enable

# Sprite color = white
code.extend([0xA9, 0x01, 0x8D, 0x27, 0xD0])  # $D027 = sprite 0 color

# Expand sprite (double size)
code.extend([0xA9, 0x01, 0x8D, 0x1D, 0xD0])  # $D01D = X expand
code.extend([0xA9, 0x01, 0x8D, 0x17, 0xD0])  # $D017 = Y expand

# Init sprite position
code.extend([0xA9, 0x64, 0x85, 0x02])  # X lo = 100
code.extend([0xA9, 0xA0, 0x85, 0x03])  # Y = 160
code.extend([0xA9, 0x00, 0x85, 0x04])  # X dir = right
code.extend([0xA9, 0x00, 0x85, 0x05])  # Y dir = down
code.extend([0xA9, 0x01, 0x85, 0x06])  # Sprite color = 1 (white)
code.extend([0xA9, 0x00, 0x8D, 0x10, 0xD0])  # X MSB = 0

# Init zero page vars
scroll_lo_idx = len(code) + 1
code.extend([0xA9, 0x00, 0x85, 0xFB])
scroll_hi_idx = len(code) + 1
code.extend([0xA9, 0x00, 0x85, 0xFC])
code.extend([0xA9, 0x00, 0x85, 0xFD, 0xA9, 0x00, 0x85, 0xFE, 0xA9, 0x00, 0x85, 0xFF])

# CLI
code.append(0x58)

# === MAIN LOOP ===
main_loop_pos = len(code)

# Wait for raster 250
wait_pos = len(code)
code.extend([0xAD, 0x12, 0xD0, 0xC9, 0xFA])
offset = (wait_pos - (len(code) + 2)) & 0xFF
code.extend([0xD0, offset])

# Raster bars
code.extend([0xA2, 0x20])
raster_pos = len(code)
code.extend([0xAD, 0x12, 0xD0, 0x29, 0x0F, 0x8D, 0x20, 0xD0, 0xCA])
offset = (raster_pos - (len(code) + 2)) & 0xFF
code.extend([0xD0, offset])
code.extend([0xA9, 0x00, 0x8D, 0x20, 0xD0])

# === SPRITE MOVEMENT ===
# Simpler approach: always update position, check bounds, change color on bounce

# Move X
code.extend([0xA5, 0x04])  # LDA X dir
code.extend([0xD0, 0x04])  # BNE go_left
code.extend([0xE6, 0x02])  # INC X (go right)
code.extend([0xD0, 0x02])  # BNE done_x (always)
code.extend([0xC6, 0x02])  # DEC X (go left)
# done_x: check bounds

# Check X bounds
code.extend([0xA5, 0x02])  # LDA X
code.extend([0xC9, 0x18])  # CMP #24 (left edge)
code.extend([0xB0, 0x06])  # BCS not_left
code.extend([0xA9, 0x00, 0x85, 0x04])  # dir = right
code.extend([0xE6, 0x06])  # INC color
# not_left:
code.extend([0xC9, 0xE0])  # CMP #224 (right edge)
code.extend([0x90, 0x06])  # BCC not_right
code.extend([0xA9, 0x01, 0x85, 0x04])  # dir = left
code.extend([0xE6, 0x06])  # INC color
# not_right:

# Move Y
code.extend([0xA5, 0x05])  # LDA Y dir
code.extend([0xD0, 0x04])  # BNE go_up
code.extend([0xE6, 0x03])  # INC Y (go down)
code.extend([0xD0, 0x02])  # BNE done_y
code.extend([0xC6, 0x03])  # DEC Y (go up)
# done_y: check bounds

# Check Y bounds
code.extend([0xA5, 0x03])  # LDA Y
code.extend([0xC9, 0x32])  # CMP #50 (top edge)
code.extend([0xB0, 0x06])  # BCS not_top
code.extend([0xA9, 0x00, 0x85, 0x05])  # dir = down
code.extend([0xE6, 0x06])  # INC color
# not_top:
code.extend([0xC9, 0xE0])  # CMP #224 (bottom edge)
code.extend([0x90, 0x06])  # BCC not_bottom
code.extend([0xA9, 0x01, 0x85, 0x05])  # dir = up
code.extend([0xE6, 0x06])  # INC color
# not_bottom:

# Wrap color to 1-15 (skip 0/black)
code.extend([0xA5, 0x06])  # LDA color
code.extend([0x29, 0x0F])  # AND #15
code.extend([0xD0, 0x02])  # BNE not_zero
code.extend([0xA9, 0x01])  # LDA #1
code.extend([0x85, 0x06])  # STA color

# Store sprite position and color to VIC
code.extend([0xA5, 0x02, 0x8D, 0x00, 0xD0])  # Sprite 0 X
code.extend([0xA5, 0x03, 0x8D, 0x01, 0xD0])  # Sprite 0 Y
code.extend([0xA5, 0x06, 0x8D, 0x27, 0xD0])  # Sprite 0 color

# === MUSIC ===
code.extend([0xE6, 0xFF, 0xA5, 0xFF, 0x29, 0x0B])  # Slower tempo (every 12 frames)
music_bne_idx = len(code) + 1
code.extend([0xD0, 0x00])

music_start = len(code)
code.extend([0xA6, 0xFE])

# V1 - Triangle wave (0x10/0x11) for flute-like Japanese sound
code.extend([0xA9, 0x10, 0x8D, 0x04, 0xD4])  # Gate off, triangle
mel_lo_idx = len(code) + 1
code.extend([0xBD, 0x00, 0x00, 0x8D, 0x00, 0xD4])
mel_hi_idx = len(code) + 1
code.extend([0xBD, 0x00, 0x00, 0x8D, 0x01, 0xD4])
code.extend([0xA9, 0x11, 0x8D, 0x04, 0xD4])  # Gate on, triangle

# V2
code.extend([0xA9, 0x20, 0x8D, 0x0B, 0xD4])
bass_lo_idx = len(code) + 1
code.extend([0xBD, 0x00, 0x00, 0x8D, 0x07, 0xD4])
bass_hi_idx = len(code) + 1
code.extend([0xBD, 0x00, 0x00, 0x8D, 0x08, 0xD4])
code.extend([0xA9, 0x21, 0x8D, 0x0B, 0xD4])

# V3 drums
code.extend([0xA9, 0x80, 0x8D, 0x12, 0xD4])
drum_lo_idx = len(code) + 1
code.extend([0xBD, 0x00, 0x00, 0x8D, 0x0E, 0xD4])
drum_hi_idx = len(code) + 1
code.extend([0xBD, 0x00, 0x00, 0x8D, 0x0F, 0xD4])
code.extend([0xA9, 0x81, 0x8D, 0x12, 0xD4])

# Inc music index
code.extend([0xE6, 0xFE, 0xA5, 0xFE, 0xC9, len(MELODY), 0xD0, 0x04, 0xA9, 0x00, 0x85, 0xFE])

music_end = len(code)
code[music_bne_idx] = (music_end - music_bne_idx - 1) & 0xFF

# === SCROLL ===
code.extend([0xE6, 0xFD, 0xA5, 0xFD, 0x29, 0x03])
scroll_bne_idx = len(code) + 1
code.extend([0xD0, 0x00])

scroll_code_start = len(code)
code.extend([0xA2, 0x00])
shift_pos = len(code)
code.extend([0xBD, 0xC1, 0x07, 0x9D, 0xC0, 0x07, 0xBD, 0xC1, 0xDB, 0x9D, 0xC0, 0xDB, 0xE8, 0xE0, 0x27])
offset = (shift_pos - (len(code) + 2)) & 0xFF
code.extend([0xD0, offset])

code.extend([0xA0, 0x00, 0xB1, 0xFB, 0xD0, 0x08])
reset_lo_idx = len(code) + 1
code.extend([0xA9, 0x00, 0x85, 0xFB])
reset_hi_idx = len(code) + 1
code.extend([0xA9, 0x00, 0x85, 0xFC])
code.extend([0xB1, 0xFB])

code.extend([0x8D, 0xE7, 0x07, 0xA9, 0x0E, 0x8D, 0xE7, 0xDB])
code.extend([0xE6, 0xFB, 0xD0, 0x02, 0xE6, 0xFC])

# JMP main
jmp_pos = len(code)
main_addr = BASE + main_loop_pos
code.extend([0x4C, lo(main_addr), hi(main_addr)])

code[scroll_bne_idx] = (jmp_pos - scroll_bne_idx - 1) & 0xFF

# === DATA ===

# Sprite data must be at 64-byte aligned address
# We'll put it at $0340 (block 13, which is 13*64 = 832 = $0340)
# First, pad to align code so sprite is at $0340
# $0340 is within $0000-$07FF which is the default VIC bank

# For simplicity, store sprite data in our code segment and copy it to $0340 at init
# Actually, let's put data at end and copy during init

scroll_addr = BASE + len(code)
code.extend(text_to_petscii(scroll))
code.append(0)

mel_lo_addr = BASE + len(code)
for n in MELODY: code.append(SID_NOTES[n][1])
mel_hi_addr = BASE + len(code)
for n in MELODY: code.append(SID_NOTES[n][0])

bass_lo_addr = BASE + len(code)
for n in BASS: code.append(SID_NOTES[n][1])
bass_hi_addr = BASE + len(code)
for n in BASS: code.append(SID_NOTES[n][0])

drum_freqs = {0:(0,0), 1:(0x05,0), 2:(0x30,0), 3:(0xA0,0)}
drum_lo_addr = BASE + len(code)
for d in DRUMS: code.append(drum_freqs[d][1])
drum_hi_addr = BASE + len(code)
for d in DRUMS: code.append(drum_freqs[d][0])

# Sprite data
sprite_data_addr = BASE + len(code)
code.extend(SPRITE_DATA)
while len(code) % 64 != 0:  # Pad to 64 bytes
    code.append(0)

# Patch all refs
code[scroll_lo_idx] = lo(scroll_addr)
code[scroll_hi_idx] = hi(scroll_addr)
code[reset_lo_idx] = lo(scroll_addr)
code[reset_hi_idx] = hi(scroll_addr)
code[mel_lo_idx] = lo(mel_lo_addr)
code[mel_lo_idx+1] = hi(mel_lo_addr)
code[mel_hi_idx] = lo(mel_hi_addr)
code[mel_hi_idx+1] = hi(mel_hi_addr)
code[bass_lo_idx] = lo(bass_lo_addr)
code[bass_lo_idx+1] = hi(bass_lo_addr)
code[bass_hi_idx] = lo(bass_hi_addr)
code[bass_hi_idx+1] = hi(bass_hi_addr)
code[drum_lo_idx] = lo(drum_lo_addr)
code[drum_lo_idx+1] = hi(drum_lo_addr)
code[drum_hi_idx] = lo(drum_hi_addr)
code[drum_hi_idx+1] = hi(drum_hi_addr)

# Calculate sprite block number (sprite_data_addr / 64)
sprite_block = sprite_data_addr // 64
code[sprite_block_idx] = sprite_block

prg.extend(code)

with open('demo.prg', 'wb') as f:
    f.write(bytes(prg))

print(f"Created demo.prg ({len(prg)} bytes)")
print(f"Sprite at ${sprite_data_addr:04X} (block {sprite_block})")
print("x64 demo.prg, then RUN")
