#!/usr/bin/env python3

# Disassembler for NXP's secret "EZH" microprocessor (aka IOH Arch. B, aka SmartDMA)
# Copyright (c) 2023 Aedan Cullen <aedan@aedancullen.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import ezh_prv

def dis_word(fh, x):
    sel_mnemonic = None
    sel_fields = None
    for (mnemonic, codemask, code, fields) in ezh_prv.INST:
        if (x ^ code) & codemask == 0:
            if sel_mnemonic != None:
                print("prev sel_mnemonic:\t\t", sel_mnemonic)
                print("new sel_mnemonic:\t\t", mnemonic)
                print("duplicate mnemonic match; exiting")
                sys.exit(1)
            sel_mnemonic = mnemonic
            sel_fields = fields
    if sel_mnemonic == None:
        fh.write("E_NOP\t\t\t\t\t\t\t\t\t\t// Unknown instruction\n")
    else:
        fh.write(sel_mnemonic)
        if sel_fields == []:
            fh.write("\n")
            return
        fh.write("(")
        i = 0
        for field_decoder in sel_fields:
            if i != 0:
                fh.write(", ")
            fh.write(str(field_decoder(x)))
            i += 1
        fh.write(")\n")

base_file = sys.argv[-1]
bin_file = base_file

if sys.argv[1] == "-p":
    with open(base_file, "r") as fh:
        res = fh.read()
    res = res.replace("{", "[")
    res = res.replace("}", "]")
    res = res.replace("U", "")
    res = eval(res)
    bin_file = base_file + ".bin"
    with open(bin_file, "wb") as fh:
        for byte in res:
            fh.write(byte.to_bytes())
    print("Wrote binary", bin_file)

disas_file = base_file + ".h"

with open(bin_file, "rb") as fh:
    with open(disas_file, "w") as dis_out:
        dis_out.write("// Generated by ezhdis.py from ")
        dis_out.write(bin_file)
        dis_out.write("\n\n")
        dis_out.write('#include "fsl_smartdma_prv.h"\n\n')
        word = fh.read(4)
        while word:
            x = int.from_bytes(word, "little")
            dis_word(dis_out, x)
            word = fh.read(4)
print("Wrote disassembly", disas_file)