# C64 Demo Project

## Overview
Classic Commodore 64 cracktro-style demo featuring:
- Raster color bar effects
- Scrolling text message
- 3-channel SID music (Last Ninja Japanese style)
- Bouncing Pulumi logo sprite with color cycling

## Files
- `demo.prg` - Compiled C64 program (~1745 bytes)
- `demo.d64` - D64 disk image for emulator compatibility
- `build_demo.py` - Python script that generates the .prg file
- `make_d64.py` - Creates D64 disk image from .prg
- `png2sprite.py` - Converts PNG images to C64 sprite data
- `demo.asm` - 6502 assembly source (reference only)
- `avatar-on-white.png` - Pulumi logo source image

## Build
```bash
python3 build_demo.py    # Creates demo.prg
python3 make_d64.py      # Creates demo.d64 (optional)
```
No external assembler required - the Python script hand-assembles the 6502 code.

## Run
```bash
# VICE emulator
x64 demo.prg
# Then type: RUN

# VirtualC64
# Drag demo.d64 onto window, then:
LOAD"*",8,1
RUN
```

## Technical Details

### Memory Map
- `$0801` - BASIC stub with `SYS 2064`
- `$0810` - Main program entry point
- Zero page usage:
  - `$02` - Sprite X position
  - `$03` - Sprite Y position
  - `$04` - Sprite X direction
  - `$05` - Sprite Y direction
  - `$06` - Sprite color
  - `$FB-$FC` - Scroll text pointer
  - `$FD` - Scroll counter
  - `$FE` - Music index
  - `$FF` - Frame counter

### C64 Hardware Used
- Screen RAM: `$0400`
- Color RAM: `$D800`
- VIC-II: `$D000-$D02E` (sprites, raster, border, background)
- SID: `$D400-$D418` (3-voice sound)
- Sprite pointer: `$07F8`

### Effects

1. **Raster bars** - Border color changes synced to raster line
2. **Bouncing sprite** - Pulumi logo bounces off screen edges
3. **Color cycling** - Sprite changes color on each bounce (1-15, skips black)
4. **Scroll text** - Bottom line scrolls left with message

### SID Music (Last Ninja Japanese Style)

Three voices with distinct roles:
- **Voice 1 (Lead)**: Triangle wave, Japanese "In" scale (E, F, A, B, C)
  - Soft attack ADSR for flute-like shakuhachi sound
- **Voice 2 (Bass)**: Sawtooth wave, sparse octave hits
  - Deep, punchy sound with full sustain
- **Voice 3 (Drums)**: Noise wave, taiko-style patterns
  - Kick, rim clicks, and sparse fills

64-note patterns with slower tempo for atmospheric feel.

### Sprite Details
- 24x21 pixels, monochrome (single color)
- Pulumi logo: 9 ovals in diamond/cube arrangement
- Double-sized (X and Y expanded)
- Position stored in zero page, updated each frame

### PETSCII
Text uses PETSCII screen codes (not ASCII). The `text_to_petscii()` function handles conversion.

## Modifying

### Change scroll text
Edit `scroll` variable in `build_demo.py` and rebuild.

### Change music
Edit `MELODY`, `BASS`, and `DRUMS` arrays. Notes use format like `'E4'`, `'A3'`, `'REST'`.

### Change sprite
Edit `SPRITE_DATA` array (21 rows of 3 bytes each = 63 bytes).
Or use `png2sprite.py` to convert a PNG image.

### Change colors
- Raster: modify the raster bar loop
- Text: change color values in print loops (0-15)
- Sprite: starts at color 1, cycles through 1-15 on bounce

### C64 Color Codes
```
0=black, 1=white, 2=red, 3=cyan, 4=purple, 5=green,
6=blue, 7=yellow, 8=orange, 9=brown, 10=light red,
11=dark gray, 12=gray, 13=light green, 14=light blue, 15=light gray
```

## SID Note Reference
```
Octave 2: C2, D2, E2, F2, G2, A2, B2 (bass range)
Octave 3: C3, D3, E3, F3, G3, A3, B3
Octave 4: C4, D4, E4, F4, G4, A4, B4 (melody range)
Octave 5: C5, D5, E5, F5, G5, A5
REST = silence
```
