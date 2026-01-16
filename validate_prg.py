#!/usr/bin/env python3
"""
C64 PRG Validator - Validates PRG file structure without running an emulator
"""

import sys

# 6502 Opcodes for basic disassembly
OPCODES = {
    0x00: ('BRK', 1), 0x01: ('ORA (zp,X)', 2), 0x05: ('ORA zp', 2), 0x06: ('ASL zp', 2),
    0x08: ('PHP', 1), 0x09: ('ORA #', 2), 0x0A: ('ASL A', 1), 0x0D: ('ORA abs', 3),
    0x0E: ('ASL abs', 3), 0x10: ('BPL rel', 2), 0x18: ('CLC', 1), 0x19: ('ORA abs,Y', 3),
    0x1D: ('ORA abs,X', 3), 0x20: ('JSR abs', 3), 0x21: ('AND (zp,X)', 2),
    0x24: ('BIT zp', 2), 0x25: ('AND zp', 2), 0x26: ('ROL zp', 2), 0x28: ('PLP', 1),
    0x29: ('AND #', 2), 0x2A: ('ROL A', 1), 0x2C: ('BIT abs', 3), 0x2D: ('AND abs', 3),
    0x30: ('BMI rel', 2), 0x38: ('SEC', 1), 0x39: ('AND abs,Y', 3), 0x3D: ('AND abs,X', 3),
    0x40: ('RTI', 1), 0x41: ('EOR (zp,X)', 2), 0x45: ('EOR zp', 2), 0x46: ('LSR zp', 2),
    0x48: ('PHA', 1), 0x49: ('EOR #', 2), 0x4A: ('LSR A', 1), 0x4C: ('JMP abs', 3),
    0x4D: ('EOR abs', 3), 0x50: ('BVC rel', 2), 0x58: ('CLI', 1), 0x59: ('EOR abs,Y', 3),
    0x5D: ('EOR abs,X', 3), 0x60: ('RTS', 1), 0x61: ('ADC (zp,X)', 2), 0x65: ('ADC zp', 2),
    0x66: ('ROR zp', 2), 0x68: ('PLA', 1), 0x69: ('ADC #', 2), 0x6A: ('ROR A', 1),
    0x6C: ('JMP (abs)', 3), 0x6D: ('ADC abs', 3), 0x70: ('BVS rel', 2), 0x78: ('SEI', 1),
    0x79: ('ADC abs,Y', 3), 0x7D: ('ADC abs,X', 3), 0x81: ('STA (zp,X)', 2),
    0x84: ('STY zp', 2), 0x85: ('STA zp', 2), 0x86: ('STX zp', 2), 0x88: ('DEY', 1),
    0x8A: ('TXA', 1), 0x8C: ('STY abs', 3), 0x8D: ('STA abs', 3), 0x8E: ('STX abs', 3),
    0x90: ('BCC rel', 2), 0x91: ('STA (zp),Y', 2), 0x94: ('STY zp,X', 2),
    0x95: ('STA zp,X', 2), 0x96: ('STX zp,Y', 2), 0x98: ('TYA', 1), 0x99: ('STA abs,Y', 3),
    0x9A: ('TXS', 1), 0x9D: ('STA abs,X', 3), 0xA0: ('LDY #', 2), 0xA1: ('LDA (zp,X)', 2),
    0xA2: ('LDX #', 2), 0xA4: ('LDY zp', 2), 0xA5: ('LDA zp', 2), 0xA6: ('LDX zp', 2),
    0xA8: ('TAY', 1), 0xA9: ('LDA #', 2), 0xAA: ('TAX', 1), 0xAC: ('LDY abs', 3),
    0xAD: ('LDA abs', 3), 0xAE: ('LDX abs', 3), 0xB0: ('BCS rel', 2), 0xB1: ('LDA (zp),Y', 2),
    0xB4: ('LDY zp,X', 2), 0xB5: ('LDA zp,X', 2), 0xB6: ('LDX zp,Y', 2), 0xB8: ('CLV', 1),
    0xB9: ('LDA abs,Y', 3), 0xBA: ('TSX', 1), 0xBC: ('LDY abs,X', 3), 0xBD: ('LDA abs,X', 3),
    0xBE: ('LDX abs,Y', 3), 0xC0: ('CPY #', 2), 0xC1: ('CMP (zp,X)', 2), 0xC4: ('CPY zp', 2),
    0xC5: ('CMP zp', 2), 0xC6: ('DEC zp', 2), 0xC8: ('INY', 1), 0xC9: ('CMP #', 2),
    0xCA: ('DEX', 1), 0xCC: ('CPY abs', 3), 0xCD: ('CMP abs', 3), 0xCE: ('DEC abs', 3),
    0xD0: ('BNE rel', 2), 0xD1: ('CMP (zp),Y', 2), 0xD5: ('CMP zp,X', 2),
    0xD6: ('DEC zp,X', 2), 0xD8: ('CLD', 1), 0xD9: ('CMP abs,Y', 3), 0xDD: ('CMP abs,X', 3),
    0xDE: ('DEC abs,X', 3), 0xE0: ('CPX #', 2), 0xE1: ('SBC (zp,X)', 2), 0xE4: ('CPX zp', 2),
    0xE5: ('SBC zp', 2), 0xE6: ('INC zp', 2), 0xE8: ('INX', 1), 0xE9: ('SBC #', 2),
    0xEA: ('NOP', 1), 0xEC: ('CPX abs', 3), 0xED: ('SBC abs', 3), 0xEE: ('INC abs', 3),
    0xF0: ('BEQ rel', 2), 0xF1: ('SBC (zp),Y', 2), 0xF5: ('SBC zp,X', 2),
    0xF6: ('INC zp,X', 2), 0xF8: ('SED', 1), 0xF9: ('SBC abs,Y', 3), 0xFD: ('SBC abs,X', 3),
    0xFE: ('INC abs,X', 3),
}

def validate_prg(filename):
    """Validate a C64 PRG file structure"""
    print(f"=== C64 PRG Validator ===")
    print(f"File: {filename}\n")

    try:
        with open(filename, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"ERROR: File not found: {filename}")
        return False

    if len(data) < 10:
        print("ERROR: File too small to be a valid PRG")
        return False

    # Check load address
    load_addr = data[0] | (data[1] << 8)
    print(f"Load address: ${load_addr:04X}")

    if load_addr == 0x0801:
        print("  [OK] Standard BASIC start address")
    elif load_addr == 0x0800:
        print("  [OK] Alternate BASIC address")
    elif load_addr >= 0xC000:
        print("  [WARN] High memory address (cartridge/kernel area)")
    else:
        print(f"  [INFO] Non-standard load address")

    # Check for BASIC stub
    print(f"\nBASIC Stub Analysis:")
    if load_addr == 0x0801:
        # Check BASIC line structure
        next_line = data[2] | (data[3] << 8)
        line_num = data[4] | (data[5] << 8)
        print(f"  Next line ptr: ${next_line:04X}")
        print(f"  Line number: {line_num}")

        # Check for SYS token (0x9E)
        if data[6] == 0x9E:
            print("  [OK] SYS token found")
            # Extract SYS address from ASCII digits
            sys_str = ""
            i = 7
            while i < len(data) and data[i] != 0:
                sys_str += chr(data[i])
                i += 1
            try:
                sys_addr = int(sys_str)
                print(f"  SYS address: {sys_addr} (${sys_addr:04X})")

                # Calculate offset to machine code
                code_offset = sys_addr - load_addr + 2  # +2 for load address bytes
                print(f"  Code starts at file offset: {code_offset}")
            except:
                print(f"  [WARN] Could not parse SYS address: {sys_str}")
        else:
            print(f"  [WARN] Expected SYS token (0x9E), got 0x{data[6]:02X}")

    # File size analysis
    print(f"\nFile Size:")
    print(f"  Total: {len(data)} bytes")
    print(f"  Code/data: {len(data) - 2} bytes (excluding load address)")

    # Memory usage
    end_addr = load_addr + len(data) - 2
    print(f"  Memory range: ${load_addr:04X} - ${end_addr:04X}")

    if end_addr > 0x9FFF:
        print("  [WARN] Extends beyond BASIC RAM")
    elif end_addr > 0x0800 + 38911:
        print("  [WARN] Larger than typical BASIC program area")
    else:
        print("  [OK] Fits in BASIC RAM area")

    # Disassemble first few instructions
    print(f"\nFirst 20 instructions (from entry point):")
    print("-" * 50)

    # Start disassembly from SYS target
    try:
        sys_str = ""
        i = 7
        while i < len(data) and data[i] != 0:
            sys_str += chr(data[i])
            i += 1
        sys_addr = int(sys_str)
        code_offset = sys_addr - load_addr + 2
    except:
        code_offset = 15  # Default to after BASIC stub
        sys_addr = load_addr + code_offset - 2

    pc = sys_addr
    file_pos = code_offset
    instr_count = 0
    valid_instructions = 0

    while instr_count < 20 and file_pos < len(data):
        opcode = data[file_pos]

        if opcode in OPCODES:
            mnemonic, size = OPCODES[opcode]
            valid_instructions += 1

            if size == 1:
                print(f"  ${pc:04X}: {opcode:02X}       {mnemonic}")
            elif size == 2:
                if file_pos + 1 < len(data):
                    operand = data[file_pos + 1]
                    print(f"  ${pc:04X}: {opcode:02X} {operand:02X}    {mnemonic} ${operand:02X}")
                else:
                    print(f"  ${pc:04X}: {opcode:02X}       {mnemonic} ???")
            elif size == 3:
                if file_pos + 2 < len(data):
                    lo = data[file_pos + 1]
                    hi = data[file_pos + 2]
                    addr = lo | (hi << 8)
                    print(f"  ${pc:04X}: {opcode:02X} {lo:02X} {hi:02X} {mnemonic} ${addr:04X}")
                else:
                    print(f"  ${pc:04X}: {opcode:02X}       {mnemonic} ???")

            file_pos += size
            pc += size
        else:
            print(f"  ${pc:04X}: {opcode:02X}       ??? (unknown opcode)")
            file_pos += 1
            pc += 1

        instr_count += 1

    # Validation summary
    print(f"\n=== Validation Summary ===")
    valid = True

    if load_addr != 0x0801:
        print("[WARN] Non-standard load address")

    if valid_instructions < 15:
        print(f"[WARN] Only {valid_instructions}/20 valid opcodes in entry code")
        valid = False
    else:
        print(f"[OK] {valid_instructions}/20 valid opcodes found")

    # Check for common patterns
    has_sei = 0x78 in data[code_offset:code_offset+50]
    has_cli = 0x58 in data[code_offset:code_offset+100]
    has_jmp = 0x4C in data[code_offset:code_offset+500]

    if has_sei:
        print("[OK] SEI (disable interrupts) found - typical for demos")
    if has_jmp:
        print("[OK] JMP instruction found - has main loop")

    # Check for VIC-II and SID access
    vic_access = False
    sid_access = False
    for i in range(2, len(data) - 2):
        if data[i] == 0xD0 and data[i-1] in range(0x00, 0x30):
            vic_access = True
        if data[i] == 0xD4 and data[i-1] in range(0x00, 0x19):
            sid_access = True

    if vic_access:
        print("[OK] VIC-II ($D0xx) access detected - graphics code present")
    if sid_access:
        print("[OK] SID ($D4xx) access detected - sound code present")

    print(f"\nResult: {'VALID PRG' if valid else 'POSSIBLE ISSUES'}")
    return valid

if __name__ == '__main__':
    filename = sys.argv[1] if len(sys.argv) > 1 else 'demo.prg'
    validate_prg(filename)
