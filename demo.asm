; C64 Cracktro-style Demo
; Classic demoscene intro with raster bars and scroller

; C64 Memory locations
SCREEN      = $0400     ; Screen memory
COLORRAM    = $d800     ; Color RAM
BORDER      = $d020     ; Border color
BACKGROUND  = $d021     ; Background color
RASTER      = $d012     ; Raster line
IRQFLAG     = $d019     ; Interrupt flag register
IRQENABLE   = $d01a     ; Interrupt enable register
IRQVECLO    = $0314     ; IRQ vector low byte
IRQVECHI    = $0315     ; IRQ vector high byte
VICCTRL     = $d011     ; VIC control register

; Zero page variables
SCROLLPOS   = $02       ; Scroll position counter
TEXTPTR     = $03       ; Text pointer (2 bytes)
COLORCYCLE  = $05       ; Color cycle counter
RASTERCNT   = $06       ; Raster effect counter

            * = $0801   ; BASIC start address

; BASIC stub: 10 SYS 2064
            .word nextline
            .word 10            ; Line number
            .byte $9e           ; SYS token
            .text "2064"        ; Address as ASCII
            .byte 0             ; End of line
nextline    .word 0             ; End of BASIC program

; Main program starts at $0810 (2064)
            * = $0810

start:
            sei                 ; Disable interrupts

            ; Clear screen
            ldx #0
            lda #32             ; Space character
clrscr:     sta SCREEN,x
            sta SCREEN+$100,x
            sta SCREEN+$200,x
            sta SCREEN+$2e8,x
            lda #0              ; Black color
            sta COLORRAM,x
            sta COLORRAM+$100,x
            sta COLORRAM+$200,x
            sta COLORRAM+$2e8,x
            lda #32
            inx
            bne clrscr

            ; Set black background and border
            lda #0
            sta BORDER
            sta BACKGROUND

            ; Print title text
            ldx #0
printtitle: lda titletext,x
            beq titleend
            sta SCREEN+44,x     ; Row 1, centered
            lda #1              ; White color
            sta COLORRAM+44,x
            inx
            bne printtitle
titleend:

            ; Print "CRACKED BY" text
            ldx #0
printcrack: lda crackedtext,x
            beq crackend
            sta SCREEN+172,x    ; Row 4, centered
            lda #7              ; Yellow color
            sta COLORRAM+172,x
            inx
            bne printcrack
crackend:

            ; Print crew name with color cycling setup
            ldx #0
printcrew:  lda crewtext,x
            beq crewend
            sta SCREEN+254,x    ; Row 6, centered
            lda #2              ; Red color initially
            sta COLORRAM+254,x
            inx
            bne printcrew
crewend:

            ; Print "PRESENTS" text
            ldx #0
printpres:  lda presentstext,x
            beq presend
            sta SCREEN+336,x    ; Row 8, centered
            lda #5              ; Green color
            sta COLORRAM+336,x
            inx
            bne printpres
presend:

            ; Initialize scroll variables
            lda #0
            sta SCROLLPOS
            sta COLORCYCLE
            lda #<scrolltext
            sta TEXTPTR
            lda #>scrolltext
            sta TEXTPTR+1

            ; Set up raster interrupt
            lda #$7f
            sta $dc0d           ; Disable CIA interrupts
            sta $dd0d
            lda $dc0d           ; Clear pending
            lda $dd0d

            lda #$01
            sta IRQENABLE       ; Enable raster interrupt

            lda #$1b
            sta VICCTRL         ; Clear high bit of raster
            lda #$00            ; Raster line 0
            sta RASTER

            lda #<irqhandler
            sta IRQVECLO
            lda #>irqhandler
            sta IRQVECHI

            cli                 ; Enable interrupts

            ; Main loop - just wait
mainloop:   jmp mainloop

; IRQ Handler - raster effects and scrolling
irqhandler:
            lda RASTER
            cmp #50
            bcc doraster
            cmp #250
            bcs endeffects

            ; Middle section - do scroll
            jsr doscroll
            jmp endeffects

doraster:
            ; Raster bar effect at top
            ldx RASTER
            lda rastertable,x
            sta BORDER

endeffects:
            ; Color cycle the crew name
            inc COLORCYCLE
            lda COLORCYCLE
            and #$07
            beq docycle
            jmp irqdone

docycle:
            ldx #0
            lda COLORRAM+254
            tay
cycleloop:  lda COLORRAM+255,x
            sta COLORRAM+254,x
            inx
            cpx #15
            bne cycleloop
            tya
            sta COLORRAM+254+15

irqdone:
            asl IRQFLAG         ; Acknowledge interrupt
            jmp $ea31           ; Return via kernal

; Scroll routine
doscroll:
            inc SCROLLPOS
            lda SCROLLPOS
            cmp #8
            bne scrolldone

            lda #0
            sta SCROLLPOS

            ; Shift scroll line left
            ldx #0
shiftloop:  lda SCREEN+960+1,x
            sta SCREEN+960,x
            lda COLORRAM+960+1,x
            sta COLORRAM+960,x
            inx
            cpx #39
            bne shiftloop

            ; Get next character
            ldy #0
            lda (TEXTPTR),y
            bne notend

            ; Reset to start of text
            lda #<scrolltext
            sta TEXTPTR
            lda #>scrolltext
            sta TEXTPTR+1
            lda (TEXTPTR),y

notend:     sta SCREEN+999
            lda #14             ; Light blue
            sta COLORRAM+999

            ; Increment text pointer
            inc TEXTPTR
            bne scrolldone
            inc TEXTPTR+1

scrolldone: rts

; Raster color table
rastertable:
            .byte 0,0,0,0,0,0,6,6,14,14,3,3,1,1,1,1
            .byte 1,1,3,3,14,14,6,6,0,0,0,0,0,0,4,4
            .byte 10,10,7,7,1,1,1,1,7,7,10,10,4,4,0,0
            .byte 0,0

; Text data
titletext:
            .text "*** CLASSIC C64 DEMO ***"
            .byte 0

crackedtext:
            .text "ORIGINAL CRACK BY"
            .byte 0

crewtext:
            .text "CLAUDE CODERS!!"
            .byte 0

presentstext:
            .text "- PRESENTS -"
            .byte 0

scrolltext:
            .text "    WELCOME TO THIS CLASSIC C64 DEMO! "
            .text "GREETINGS FLY OUT TO ALL THE OLD SCHOOL CREWS... "
            .text "FAIRLIGHT, TRIAD, CENSOR, HOTLINE, IKARI AND MANY MORE! "
            .text "LONG LIVE THE COMMODORE 64 AND THE DEMO SCENE! "
            .text "THIS DEMO WAS CODED IN 2024 BUT WITH LOVE FOR THE 80S! "
            .text "KEEP THE SPIRIT ALIVE...      "
            .byte 0
