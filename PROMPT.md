# Ultimate C64 Cracktro - Ralph Loop Task

Build a legendary Commodore 64 cracktro in the style of **Fairlight**, **Triad**, and **Dominators**.

## Required Text (MUST INCLUDE)

```
ENGIN DIRI X:_EDIRI GITHUB:DIRIEN ... INFRASTRUCTURE AS CODE CREW RULES THE WORLD!
```

Crew name: **"IAC CREW"**

---

## Phases (Complete in Order)

### Phase 1: Foundation & Music
- [x] Verify `python3 build_demo.py` produces working `demo.prg`
- [x] Update scroll text to required message above
- [x] Enhance SID music: 3 voices, arpeggios, filter sweeps, punchy bass
- [x] Music should loop seamlessly with no clicks/pops

**Checkpoint:** Run `python3 build_demo.py` - demo loads and music plays. ✓

### Phase 2: Enhanced Raster Bars
- [x] Improve raster bar effect with smoother color cycling
- [x] Add rainbow gradient (cycle through all 16 C64 colors)
- [x] Sync raster bars to stable raster timing

**Checkpoint:** Raster bars cycle smoothly without flickering. ✓

### Phase 3: Sine Wave Scroller
- [x] Convert flat scroll text to DYCP sine wave scroller
- [x] Each character at different Y position following sine curve
- [x] Smooth pixel scrolling (not character-by-character)

**Checkpoint:** Scroll text waves vertically in sine pattern. ✓

### Phase 4: Starfield Effect
- [x] Add parallax starfield background (at least 2 layers)
- [x] Stars move at different speeds for depth
- [x] Use character-based stars (faster) or sprite stars

**Checkpoint:** Stars scroll behind main content. ✓

### Phase 5: Polish & Greetings
- [x] Add greetings: "GREETS TO CLOUD ENGINEERS - PULUMI CREW - FAIRLIGHT - TRIAD"
- [x] Ensure sprite bounces smoothly with color cycling
- [x] Final optimization pass for smooth 50/60Hz operation

**Checkpoint:** All effects run together without slowdown. ✓

---

## Development Loop (Follow Each Iteration)

1. Read `build_demo.py` to understand current state
2. Check which phase is incomplete (look at checkpoints above)
3. Implement ONE improvement toward current phase
4. Run: `python3 build_demo.py`
5. If build fails: fix the error immediately
6. If build succeeds: verify effect works as expected
7. Commit with message describing the change
8. Update progress below
9. Continue to next improvement

---

## Progress Tracking

Update this section each iteration:

**Current Phase:** COMPLETE
**Last Change:** All 5 phases completed - cracktro fully functional
**Status:** COMPLETE

---

## Technical Reference

### Memory Map
```
$0801 - BASIC stub (SYS 2064)
$0810 - Main program entry
$0340 - Sprite data (64-byte aligned)
$0400 - Screen RAM
$D800 - Color RAM
$D000-$D02E - VIC-II registers
$D400-$D418 - SID registers
```

### Key VIC-II Registers
- `$D012` - Current raster line
- `$D020` - Border color
- `$D021` - Background color
- `$D016` - Horizontal scroll (bits 0-2)
- `$D015` - Sprite enable
- `$D027` - Sprite 0 color

### Key SID Registers
- `$D400-$D401` - Voice 1 frequency
- `$D404` - Voice 1 control (waveform + gate)
- `$D405-$D406` - Voice 1 ADSR
- `$D418` - Volume + filter mode

### C64 Colors
```
0=black, 1=white, 2=red, 3=cyan, 4=purple, 5=green,
6=blue, 7=yellow, 8=orange, 9=brown, 10=lt red,
11=dk gray, 12=gray, 13=lt green, 14=lt blue, 15=lt gray
```

---

## Completion Criteria (ALL must be true)

1. `python3 build_demo.py` succeeds without errors
2. All 5 phases marked complete above
3. Demo runs in VICE without crashes
4. Music plays continuously (no silence gaps)
5. Raster bars cycle smoothly in border
6. Scroll text displays with sine wave motion
7. Starfield visible behind main content
8. Required text "ENGIN DIRI..." appears in scroller

---

## Escape Hatch

If stuck on a phase for 3+ iterations:
1. Document what's blocking progress in this file
2. Simplify the effect (e.g., fewer stars, simpler sine)
3. Move to next phase and return later
4. If truly blocked, output: `<promise>BLOCKED</promise>`

---

## When Complete

After ALL phases done and ALL completion criteria met, output:

<promise>COMPLETE</promise>
