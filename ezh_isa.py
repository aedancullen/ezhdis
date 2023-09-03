# ISA description of NXP's secret "EZH" microprocessor (aka IOH Arch. B, aka SmartDMA)
# Copyright (c) 2023 Aedan Cullen <aedan@aedancullen.com>
# SPDX-License-Identifier: GPL-3.0-or-later

# Unimplemented opcodes:
# 0x16 (ANDOR)
# 0x19 (register-specified shift)
# 0x1D (load/store with register-specified offset)

def signed(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)

def addr(x):
    if ENABLE_SMARTDMA_REGS:
        return SMARTDMA_REGS[x] if x in SMARTDMA_REGS else "0x%08X" % x
    return "0x%08X" % x

SMARTDMA_REGS = {
    0x00027020: "BOOT",
    0x00027024: "CTRL",
    0x00027028: "PC",
    0x0002702C: "SP",
    0x00027030: "BREAK_ADDR",
    0x00027034: "BREAK_VECT",
    0x00027038: "EMER_VECT",
    0x0002703C: "EMER_SEL",
    0x00027040: "ARM2SMARTDMA",
    0x00027044: "SMARTDMA2ARM",
    0x00027048: "PENDTRAP",
}

OPMASK = 0x1F

REG = {
    0x0: "R0",
    0x1: "R1",
    0x2: "R2",
    0x3: "R3",
    0x4: "R4",
    0x5: "R5",
    0x6: "R6",
    0x7: "R7",
    0x8: "GPO",
    0x9: "GPD",
    0xA: "CFS",
    0xB: "CFM",
    0xC: "SP",
    0xD: "PC",
    0xE: "GPI",
    0xF: "RA",
}

COND = {
    0x0: "EU",
    0x1: "ZE",
    0x2: "NZ",
    0x3: "PO",
    0x4: "NE",
    0x5: "AZ",
    0x6: "ZB",
    0x7: "CA",
    0x8: "NC",
    0x9: "CZ",
    0xA: "SPO",
    0xB: "SNE",
    0xC: "NBS",
    0xD: "NEX",
    0xE: "BS",
    0xF: "EX",
}

# (mnemonic, codemask, code, fields)

INST = [
    ("E_GOSUB", 0x3,
    0x3, [
        lambda x: addr(x & 0xFFFFFFF8),
    ]),
    ("E_NOP", 0xFF,
    0x12, [
    ]),
    ("E_INT_TRIGGER", 0xFF,
    0x14, [
        lambda x: "0x%08X" % (x >> 8),
    ]),



    ("E_COND_GOTO", OPMASK + (1 << 9) + (1 << 10),
    0x15 + (1 << 9), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: addr((x >> 9) & ~0x3),
    ]),
    ("E_COND_GOTO_REG", OPMASK + (1 << 9) + (1 << 10),
    0x15, [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
    ]),
    ("E_COND_GOTOL", OPMASK + (1 << 9) + (1 << 10),
    0x15 + (1 << 9) + (1 << 10), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: addr((x >> 9) & ~0x3),
    ]),
    ("E_COND_GOTO_REGL", OPMASK + (1 << 9) + (1 << 10),
    0x15 + (1 << 10), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
    ]),



    ("E_COND_MOV", OPMASK + (1 << 9) + (1 << 18) + (1 << 31),
    0x0, [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
    ]),
    ("E_COND_MOVS", OPMASK + (1 << 9) + (1 << 18) + (1 << 31),
    0x0 + (1 << 9), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
    ]),
    ("E_COND_MVN", OPMASK + (1 << 9) + (1 << 18) + (1 << 31),
    0x0 + (1 << 31), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
    ]),
    ("E_COND_MVNS", OPMASK + (1 << 9) + (1 << 18) + (1 << 31),
    0x0 + (1 << 9) + (1 << 31), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
    ]),
    ("E_COND_LOAD_SIMM", OPMASK + (1 << 9) + (1 << 18) + (1 << 31),
    0x0 + (1 << 18), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: signed((x >> 20) & 0x7FF, 11),
        lambda x: ((x >> 14) & 0xF) + ((x >> (19 - 4)) & 0x10),
    ]),
    ("E_COND_LOAD_SIMMS", OPMASK + (1 << 9) + (1 << 18) + (1 << 31),
    0x0 + (1 << 9) + (1 << 18), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: signed((x >> 20) & 0x7FF, 11),
        lambda x: ((x >> 14) & 0xF) + ((x >> (19 - 4)) & 0x10),
    ]),
    ("E_COND_LOAD_SIMMN", OPMASK + (1 << 9) + (1 << 18) + (1 << 31),
    0x0 + (1 << 18) + (1 << 31), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: signed((x >> 20) & 0x7FF, 11),
        lambda x: ((x >> 14) & 0xF) + ((x >> (19 - 4)) & 0x10),
    ]),
    ("E_COND_LOAD_SIMMNS", OPMASK + (1 << 9) + (1 << 18) + (1 << 31),
    0x0 + (1 << 9) + (1 << 18) + (1 << 31), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: signed((x >> 20) & 0x7FF, 11),
        lambda x: ((x >> 14) & 0xF) + ((x >> (19 - 4)) & 0x10),
    ]),



    ("E_COND_LDR", OPMASK + (1 << 18) + (1 << 19) + (1 << 20) + (1 << 21),
    0x1 + (1 << 18), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: signed((x >> 24) & 0xFF, 8),
    ]),
    ("E_COND_LDRB", OPMASK + (1 << 18) + (1 << 19) + (1 << 20) + (1 << 21),
    0x1, [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: signed((x >> 24) & 0xFF, 8),
    ]),
    ("E_COND_LDRBS", OPMASK + (1 << 18) + (1 << 19) + (1 << 20) + (1 << 21),
    0x1 + (1 << 21), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: signed((x >> 24) & 0xFF, 8),
    ]),
    ("E_COND_LDR_PRE", OPMASK + (1 << 18) + (1 << 19) + (1 << 20) + (1 << 21),
    0x1 + (1 << 18) + (1 << 20), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: signed((x >> 24) & 0xFF, 8),
    ]),
    ("E_COND_LDRB_PRE", OPMASK + (1 << 18) + (1 << 19) + (1 << 20) + (1 << 21),
    0x1 + (1 << 20), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: signed((x >> 24) & 0xFF, 8),
    ]),
    ("E_COND_LDRBS_PRE", OPMASK + (1 << 18) + (1 << 19) + (1 << 20) + (1 << 21),
    0x1 + (1 << 20) + (1 << 21), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: signed((x >> 24) & 0xFF, 8),
    ]),
    ("E_COND_LDR_POST", OPMASK + (1 << 18) + (1 << 19) + (1 << 20) + (1 << 21),
    0x1 + (1 << 18) + (1 << 19) + (1 << 20), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: signed((x >> 24) & 0xFF, 8),
    ]),
    ("E_COND_LDRB_POST", OPMASK + (1 << 18) + (1 << 19) + (1 << 20) + (1 << 21),
    0x1 + (1 << 19) + (1 << 20), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: signed((x >> 24) & 0xFF, 8),
    ]),
    ("E_COND_LDRBS_POST", OPMASK + (1 << 18) + (1 << 19) + (1 << 20) + (1 << 21),
    0x1 + (1 << 19) + (1 << 20) + (1 << 21), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: signed((x >> 24) & 0xFF, 8),
    ]),



    ("E_COND_STR", OPMASK + (1 << 18) + (1 << 19) + (1 << 10) + (1 << 11),
    0x2 + (1 << 18), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: REG[(x >> 20) & 0xF],
        lambda x: signed((x >> 24) & 0xFF, 8),
    ]),
    ("E_COND_STRB", OPMASK + (1 << 18) + (1 << 19) + (1 << 10) + (1 << 11),
    0x2, [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: REG[(x >> 20) & 0xF],
        lambda x: signed((x >> 24) & 0xFF, 8),
    ]),
    ("E_COND_STR_PRE", OPMASK + (1 << 18) + (1 << 19) + (1 << 10) + (1 << 11),
    0x2 + (1 << 18) + (1 << 10), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: REG[(x >> 20) & 0xF],
        lambda x: signed((x >> 24) & 0xFF, 8),
    ]),
    ("E_COND_STRB_PRE", OPMASK + (1 << 18) + (1 << 19) + (1 << 10) + (1 << 11),
    0x2 + (1 << 10), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: REG[(x >> 20) & 0xF],
        lambda x: signed((x >> 24) & 0xFF, 8),
    ]),
    ("E_COND_STR_POST", OPMASK + (1 << 18) + (1 << 19) + (1 << 10) + (1 << 11),
    0x2 + (1 << 18) + (1 << 19) + (1 << 10), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: REG[(x >> 20) & 0xF],
        lambda x: signed((x >> 24) & 0xFF, 8),
    ]),
    ("E_COND_STRB_POST", OPMASK + (1 << 18) + (1 << 19) + (1 << 10) + (1 << 11),
    0x2 + (1 << 19) + (1 << 10), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: REG[(x >> 20) & 0xF],
        lambda x: signed((x >> 24) & 0xFF, 8),
    ]),



    ("E_COND_PER_READ", OPMASK,
    0x4, [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: addr((x >> 12) & 0x000FFFFC),
    ]),



    ("E_COND_PER_WRITE", OPMASK,
    0x5, [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 20) & 0xF],
        lambda x: addr(((x >> 12) & 0x000FF000) + ((x >> 8) & 0x00000FFC)),
    ]),



    ("E_COND_BTST", OPMASK + (1 << 9) + (1 << 18) + (3 << 29) + (1 << 31),
    0x18 + (1 << 18) + (1 << 29) + (1 << 31), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: REG[(x >> 20) & 0xF],
    ]),
    ("E_COND_BCLR", OPMASK + (1 << 9) + (1 << 18) + (3 << 29) + (1 << 31),
    0x18 + (1 << 18) + (1 << 29), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: REG[(x >> 20) & 0xF],
    ]),
    ("E_COND_BSET", OPMASK + (1 << 9) + (1 << 18) + (3 << 29) + (1 << 31),
    0x18 + (1 << 18) + (2 << 29) + (1 << 31), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: REG[(x >> 20) & 0xF],
    ]),
    ("E_COND_BTOG", OPMASK + (1 << 9) + (1 << 18) + (3 << 29) + (1 << 31),
    0x18 + (1 << 18) + (3 << 29) + (1 << 31), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: REG[(x >> 20) & 0xF],
    ]),
    ("E_COND_BTSTS", OPMASK + (1 << 9) + (1 << 18) + (3 << 29) + (1 << 31),
    0x18 + (1 << 9) + (1 << 18) + (1 << 29) + (1 << 31), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: REG[(x >> 20) & 0xF],
    ]),
    ("E_COND_BCLRS", OPMASK + (1 << 9) + (1 << 18) + (3 << 29) + (1 << 31),
    0x18 + (1 << 9) + (1 << 18) + (1 << 29), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: REG[(x >> 20) & 0xF],
    ]),
    ("E_COND_BSETS", OPMASK + (1 << 9) + (1 << 18) + (3 << 29) + (1 << 31),
    0x18 + (1 << 9) + (1 << 18) + (2 << 29) + (1 << 31), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: REG[(x >> 20) & 0xF],
    ]),
    ("E_COND_BTOGS", OPMASK + (1 << 9) + (1 << 18) + (3 << 29) + (1 << 31),
    0x18 + (1 << 9) + (1 << 18) + (3 << 29) + (1 << 31), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: REG[(x >> 20) & 0xF],
    ]),



    ("E_COND_BTST_IMM", OPMASK + (1 << 9) + (1 << 18) + (3 << 29) + (1 << 31),
    0x18 + (1 << 29) + (1 << 31), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: (x >> 24) & 0x1F,
    ]),
    ("E_COND_BCLR_IMM", OPMASK + (1 << 9) + (1 << 18) + (3 << 29) + (1 << 31),
    0x18 + (1 << 29), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: (x >> 24) & 0x1F,
    ]),
    ("E_COND_BSET_IMM", OPMASK + (1 << 9) + (1 << 18) + (3 << 29) + (1 << 31),
    0x18 + (2 << 29) + (1 << 31), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: (x >> 24) & 0x1F,
    ]),
    ("E_COND_BTOG_IMM", OPMASK + (1 << 9) + (1 << 18) + (3 << 29) + (1 << 31),
    0x18 + (3 << 29) + (1 << 31), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: (x >> 24) & 0x1F,
    ]),
    ("E_COND_BTST_IMMS", OPMASK + (1 << 9) + (1 << 18) + (3 << 29) + (1 << 31),
    0x18 + (1 << 9) + (1 << 29) + (1 << 31), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: (x >> 24) & 0x1F,
    ]),
    ("E_COND_BCLR_IMMS", OPMASK + (1 << 9) + (1 << 18) + (3 << 29) + (1 << 31),
    0x18 + (1 << 9) + (1 << 29), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: (x >> 24) & 0x1F,
    ]),
    ("E_COND_BSET_IMMS", OPMASK + (1 << 9) + (1 << 18) + (3 << 29) + (1 << 31),
    0x18 + (1 << 9) + (2 << 29) + (1 << 31), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: (x >> 24) & 0x1F,
    ]),
    ("E_COND_BTOG_IMMS", OPMASK + (1 << 9) + (1 << 18) + (3 << 29) + (1 << 31),
    0x18 + (1 << 9) + (3 << 29) + (1 << 31), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: (x >> 24) & 0x1F,
    ]),



    ("E_COND_TIGHT_LOOP", OPMASK,
    0x1A, [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
        lambda x: REG[(x >> 20) & 0xF],
    ]),



    ("E_COND_HOLD", OPMASK + (1 << 9) + (1 << 15) + (1 << 18) + (1 << 19),
    0x1C + (1 << 15), [
        lambda x: COND[(x >> 5) & 0xF],
    ]),
    ("E_COND_VECTORED_HOLD", OPMASK + (1 << 9) + (1 << 15) + (1 << 18) + (1 << 19),
    0x1C, [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF], # table TODO check
    ]),
    ("E_COND_VECTORED_HOLD_NRA", OPMASK + (1 << 9) + (1 << 15) + (1 << 18) + (1 << 19),
    0x1C + (1 << 18), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF], # table TODO check
    ]),
    ("E_COND_VECTORED_HOLD_LV", OPMASK + (1 << 9) + (1 << 15) + (1 << 18) + (1 << 19),
    0x1C + (1 << 19), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF], # table TODO check
    ]),
    ("E_COND_VECTORED_HOLD_LV_NRA", OPMASK + (1 << 9) + (1 << 15) + (1 << 18) + (1 << 19),
    0x1C + (1 << 18) + (1 << 19), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF], # table TODO check
    ]),
    ("E_COND_ACC_VECTORED_HOLD", OPMASK + (1 << 9) + (1 << 15) + (1 << 18) + (1 << 19),
    0x1C + (1 << 9), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF], # table TODO check
        lambda x: REG[(x >> 24) & 0xF], # vectors TODO check
    ]),
    ("E_COND_ACC_VECTORED_HOLD_NRA", OPMASK + (1 << 9) + (1 << 15) + (1 << 18) + (1 << 19),
    0x1C + (1 << 9) + (1 << 18), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF], # table TODO check
        lambda x: REG[(x >> 24) & 0xF], # vectors TODO check
    ]),
    ("E_COND_ACC_VECTORED_HOLD_LV", OPMASK + (1 << 9) + (1 << 15) + (1 << 18) + (1 << 19),
    0x1C + (1 << 9) + (1 << 19), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF], # table TODO check
        lambda x: REG[(x >> 24) & 0xF], # vectors TODO check
    ]),
    ("E_COND_ACC_VECTORED_HOLD_LV_NRA", OPMASK + (1 << 9) + (1 << 15) + (1 << 18) + (1 << 19),
    0x1C + (1 << 9) + (1 << 18) + (1 << 19), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF], # table TODO check
        lambda x: REG[(x >> 24) & 0xF], # vectors TODO check
    ]),



    ("E_MODIFY_GPO_BYTE", 0xFF,
    0x1E, [
        lambda x: "0x%02X" % ((x >> 8) & 0xFF),
        lambda x: "0x%02X" % ((x >> 16) & 0xFF),
        lambda x: "0x%02X" % ((x >> 24) & 0xFF),
    ]),



    ("E_HEART_RYTHM_IMM", 0xFF + (1 << 9),
    0x32, [
        lambda x: (x >> 16) & 0xFFFF,
    ]),
    ("E_HEART_RYTHM", 0xFF + (1 << 9),
    0x32 + (1 << 9), [
        lambda x: REG[(x >> 14) & 0xF],
    ]),



    ("E_SYNCH_ALL_TO_BEAT", 0xFF,
    0x52, [
        lambda x: x >> 31,
    ]),



    ("E_WAIT_FOR_BEAT", 0xFF,
    0x72, [
    ]),
]



def build_tla1(tla, op):
    return [
        (f"E_COND_{tla}_IMM", OPMASK + (1 << 9) + (1 << 18) + (1 << 19),
        op + (1 << 18), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: signed((x >> 20) & 0xFFF, 12),
        ]),
        (f"E_COND_{tla}_IMMS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19),
        op + (1 << 9) + (1 << 18), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: signed((x >> 20) & 0xFFF, 12),
        ]),
        (f"E_COND_{tla}N_IMM", OPMASK + (1 << 9) + (1 << 18) + (1 << 19),
        op + (1 << 18) + (1 << 19), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: signed((x >> 20) & 0xFFF, 12),
        ]),
        (f"E_COND_{tla}N_IMMS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19),
        op + (1 << 9) + (1 << 18) + (1 << 19), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: signed((x >> 20) & 0xFFF, 12),
        ]),
        (f"E_COND_{tla}_LSL", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op, [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_LSLS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 9), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}N_LSL", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 19), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}N_LSLS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 9) + (1 << 19), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_LSR", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 30), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_LSRS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 9) + (1 << 30), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}N_LSR", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 19) + (1 << 30), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}N_LSRS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 9) + (1 << 19) + (1 << 30), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_ASR", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 29), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_ASRS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 9) + (1 << 29), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}N_ASR", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 19) + (1 << 29), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}N_ASRS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 9) + (1 << 19) + (1 << 29), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_ROR", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 29) + (1 << 30), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_RORS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 9) + (1 << 29) + (1 << 30), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}N_ROR", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 19) + (1 << 29) + (1 << 30), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}N_RORS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 9) + (1 << 19) + (1 << 29) + (1 << 30), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_FLSL", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 31), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_FLSLS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 9) + (1 << 31), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}N_FLSL", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 19) + (1 << 31), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}N_FLSLS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 9) + (1 << 19) + (1 << 31), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_FLSR", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 30) + (1 << 31), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_FLSRS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 9) + (1 << 30) + (1 << 31), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}N_FLSR", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 19) + (1 << 30) + (1 << 31), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}N_FLSRS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 9) + (1 << 19) + (1 << 30) + (1 << 31), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_FASR", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 29) + (1 << 31), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_FASRS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 9) + (1 << 29) + (1 << 31), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}N_FASR", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 19) + (1 << 29) + (1 << 31), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}N_FASRS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 9) + (1 << 19) + (1 << 29) + (1 << 31), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_FROR", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 29) + (1 << 30) + (1 << 31), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_FRORS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 9) + (1 << 29) + (1 << 30) + (1 << 31), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}N_FROR", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}N_FRORS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31),
        op + (1 << 9) + (1 << 19) + (1 << 29) + (1 << 30) + (1 << 31), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
    ]



INST.extend(build_tla1("ADD", 0x6))
INST.extend(build_tla1("SUB", 0x8))
INST.extend(build_tla1("ADC", 0x9))
INST.extend(build_tla1("SBC", 0xA))
INST.extend(build_tla1("OR", 0xC))
INST.extend(build_tla1("AND", 0xD))
INST.extend(build_tla1("XOR", 0XE))



def build_tla2(tla, op, field18, field19):
    return [
        (f"E_COND_{tla}", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (7 << 29),
        op + (field18 << 18) + (field19 << 19), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}S", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (7 << 29),
        op + (1 << 9) + (field18 << 18) + (field19 << 19), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_AND", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (7 << 29),
        op + (field18 << 18) + (field19 << 19) + (1 << 29), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_ANDS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (7 << 29),
        op + (1 << 9) + (field18 << 18) + (field19 << 19) + (1 << 29), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_OR", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (7 << 29),
        op + (field18 << 18) + (field19 << 19) + (2 << 29), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_ORS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (7 << 29),
        op + (1 << 9) + (field18 << 18) + (field19 << 19) + (2 << 29), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_XOR", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (7 << 29),
        op + (field18 << 18) + (field19 << 19) + (3 << 29), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_XORS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (7 << 29),
        op + (1 << 9) + (field18 << 18) + (field19 << 19) + (3 << 29), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_ADD", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (7 << 29),
        op + (field18 << 18) + (field19 << 19) + (4 << 29), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_ADDS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (7 << 29),
        op + (1 << 9) + (field18 << 18) + (field19 << 19) + (4 << 29), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_SUB", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (7 << 29),
        op + (field18 << 18) + (field19 << 19) + (5 << 29), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_SUBS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (7 << 29),
        op + (1 << 9) + (field18 << 18) + (field19 << 19) + (5 << 29), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_ADC", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (7 << 29),
        op + (field18 << 18) + (field19 << 19) + (6 << 29), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_ADCS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (7 << 29),
        op + (1 << 9) + (field18 << 18) + (field19 << 19) + (6 << 29), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_SBC", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (7 << 29),
        op + (field18 << 18) + (field19 << 19) + (7 << 29), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
        (f"E_COND_{tla}_SBCS", OPMASK + (1 << 9) + (1 << 18) + (1 << 19) + (7 << 29),
        op + (1 << 9) + (field18 << 18) + (field19 << 19) + (7 << 29), [
            lambda x: COND[(x >> 5) & 0xF],
            lambda x: REG[(x >> 10) & 0xF],
            lambda x: REG[(x >> 14) & 0xF],
            lambda x: REG[(x >> 20) & 0xF],
            lambda x: (x >> 24) & 0x1F,
        ]),
    ]



INST.extend(build_tla2("LSL", 0x10, 0, 0))
INST.extend(build_tla2("LSR", 0x10, 0, 1))
INST.extend(build_tla2("ROR", 0x10, 1, 1))
INST.extend(build_tla2("ASR", 0x10, 1, 0))
INST.extend(build_tla2("FEND_ASR", 0x11, 0, 1))
INST.extend(build_tla2("FBIT_ASR", 0x11, 1, 1))
INST.extend(build_tla2("FEND_LSR", 0x11, 0, 0))
INST.extend(build_tla2("FBIT_LSR", 0x11, 1, 0))
