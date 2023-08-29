# EZH ISA (aka IOH Arch. B, aka SmartDMA)
# Copyright (c) 2023 Aedan Cullen <aedan@aedancullen.com>
# SPDX-License-Identifier: GPL-3.0-or-later

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
        lambda x: x & ~0x3,
    ]),
    ("E_NOP", OPMASK,
    0x12, [
    ]),
    ("E_INT_TRIGGER", OPMASK,
    0x14, [
        lambda x: x >> 8,
    ]),



    ("E_COND_GOTO", OPMASK + (1 << 9) + (1 << 10),
    0x15 + (1 << 9), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: (x >> 9) & ~0x3,
    ]),
    ("E_COND_GOTO_REG", OPMASK + (1 << 9) + (1 << 10),
    0x15, [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
    ]),
    ("E_COND_GOTOL", OPMASK + (1 << 9) + (1 << 10),
    0x15 + (1 << 9) + (1 << 10), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: (x >> 9) & ~0x3,
    ]),
    ("E_COND_GOTO_REGL", OPMASK + (1 << 9) + (1 << 10),
    0x15 + (1 << 10), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
    ]),



    ("E_COND_MOV", OPMASK + (1 << 9) + (1 << 10) + (1 << 18) + (1 << 31),
    0x0, [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
    ]),
    ("E_COND_MOVS", OPMASK + (1 << 9) + (1 << 10) + (1 << 18) + (1 << 31),
    0x0 + (1 << 9), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
    ]),
    ("E_COND_MVN", OPMASK + (1 << 9) + (1 << 10) + (1 << 18) + (1 << 31),
    0x0 + (1 << 31), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
    ]),
    ("E_COND_MVNS", OPMASK + (1 << 9) + (1 << 10) + (1 << 18) + (1 << 31),
    0x0 + (1 << 9) + (1 << 31), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: REG[(x >> 14) & 0xF],
    ]),
    ("E_COND_LOAD_SIMM", OPMASK + (1 << 9) + (1 << 10) + (1 << 18) + (1 << 31),
    0x0 + (1 << 18), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: (x >> 20) & 0x7FF,
        lambda x: (x >> 14) & 0xF + (x >> (19 - 4)) & 0x10,
    ]),
    ("E_COND_LOAD_SIMMS", OPMASK + (1 << 9) + (1 << 10) + (1 << 18) + (1 << 31),
    0x0 + (1 << 9) + (1 << 18), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: (x >> 20) & 0x7FF,
        lambda x: (x >> 14) & 0xF + (x >> (19 - 4)) & 0x10,
    ]),
    ("E_COND_LOAD_SIMMN", OPMASK + (1 << 9) + (1 << 10) + (1 << 18) + (1 << 31),
    0x0 + (1 << 18), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: (x >> 20) & 0x7FF,
        lambda x: (x >> 14) & 0xF + (x >> (19 - 4)) & 0x10,
    ]),
    ("E_COND_LOAD_SIMMNS", OPMASK + (1 << 9) + (1 << 10) + (1 << 18) + (1 << 31),
    0x0 + (1 << 9) + (1 << 18), [
        lambda x: COND[(x >> 5) & 0xF],
        lambda x: REG[(x >> 10) & 0xF],
        lambda x: (x >> 20) & 0x7FF,
        lambda x: (x >> 14) & 0xF + (x >> (19 - 4)) & 0x10,
    ]),
]
