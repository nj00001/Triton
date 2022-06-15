#!/usr/bin/env python3
## -*- coding: utf-8 -*-

from __future__        import print_function

from triton            import *
from unicorn           import *
from unicorn.x86_const import *
from struct            import pack

import sys
import pprint

ADDR  = 0x100000
STACK = 0x200000
HEAP  = 0x300000
SIZE  = 5 * 1024 * 1024

CODE  = [
    (None, [], b"\x48\xb8\xaf\xbe\xad\xde\xaf\xbe\xad\xde",   "mov rax, 0xdeadbeafdeadbeaf"),
    (None, [], b"\x48\xff\xc0",                               "inc rax"),
    (None, [], b"\x48\xc7\xc3\x00\x00\x20\x00",               "mov rbx, 0x200000"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x00",                   "pextrb eax, xmm1, 0"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x01",                   "pextrb eax, xmm1, 1"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x02",                   "pextrb eax, xmm1, 2"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x03",                   "pextrb eax, xmm1, 3"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x04",                   "pextrb eax, xmm1, 4"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x05",                   "pextrb eax, xmm1, 5"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x06",                   "pextrb eax, xmm1, 6"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x07",                   "pextrb eax, xmm1, 7"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x08",                   "pextrb eax, xmm1, 8"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x09",                   "pextrb eax, xmm1, 9"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x0a",                   "pextrb eax, xmm1, 10"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x0b",                   "pextrb eax, xmm1, 11"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x0c",                   "pextrb eax, xmm1, 12"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x0d",                   "pextrb eax, xmm1, 13"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x0e",                   "pextrb eax, xmm1, 14"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x0f",                   "pextrb eax, xmm1, 15"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x10",                   "pextrb eax, xmm1, 16"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x11",                   "pextrb eax, xmm1, 17"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x12",                   "pextrb eax, xmm1, 18"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x13",                   "pextrb eax, xmm1, 19"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x14",                   "pextrb eax, xmm1, 20"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x15",                   "pextrb eax, xmm1, 21"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x16",                   "pextrb eax, xmm1, 22"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x17",                   "pextrb eax, xmm1, 23"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x18",                   "pextrb eax, xmm1, 24"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x19",                   "pextrb eax, xmm1, 25"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x1a",                   "pextrb eax, xmm1, 26"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x1b",                   "pextrb eax, xmm1, 27"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x1c",                   "pextrb eax, xmm1, 28"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x1d",                   "pextrb eax, xmm1, 29"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x1e",                   "pextrb eax, xmm1, 30"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x1f",                   "pextrb eax, xmm1, 31"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x20",                   "pextrb eax, xmm1, 32"),
    (None, [], b"\x66\x0f\x3a\x14\xc8\x21",                   "pextrb eax, xmm1, 33"),

    (None, [], b"\x66\x0f\x3a\x16\xc8\x00",                   "pextrd eax, xmm1, 0"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x01",                   "pextrd eax, xmm1, 1"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x02",                   "pextrd eax, xmm1, 2"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x03",                   "pextrd eax, xmm1, 3"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x04",                   "pextrd eax, xmm1, 4"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x05",                   "pextrd eax, xmm1, 5"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x06",                   "pextrd eax, xmm1, 6"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x07",                   "pextrd eax, xmm1, 7"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x08",                   "pextrd eax, xmm1, 8"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x09",                   "pextrd eax, xmm1, 9"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x0a",                   "pextrd eax, xmm1, 10"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x0b",                   "pextrd eax, xmm1, 11"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x0c",                   "pextrd eax, xmm1, 12"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x0d",                   "pextrd eax, xmm1, 13"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x0e",                   "pextrd eax, xmm1, 14"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x0f",                   "pextrd eax, xmm1, 15"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x10",                   "pextrd eax, xmm1, 16"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x11",                   "pextrd eax, xmm1, 17"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x12",                   "pextrd eax, xmm1, 18"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x13",                   "pextrd eax, xmm1, 19"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x14",                   "pextrd eax, xmm1, 20"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x15",                   "pextrd eax, xmm1, 21"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x16",                   "pextrd eax, xmm1, 22"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x17",                   "pextrd eax, xmm1, 23"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x18",                   "pextrd eax, xmm1, 24"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x19",                   "pextrd eax, xmm1, 25"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x1a",                   "pextrd eax, xmm1, 26"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x1b",                   "pextrd eax, xmm1, 27"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x1c",                   "pextrd eax, xmm1, 28"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x1d",                   "pextrd eax, xmm1, 29"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x1e",                   "pextrd eax, xmm1, 30"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x1f",                   "pextrd eax, xmm1, 31"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x20",                   "pextrd eax, xmm1, 32"),
    (None, [], b"\x66\x0f\x3a\x16\xc8\x21",                   "pextrd eax, xmm1, 33"),

    (None, [], b"\x66\x0f\x3a\x16\x0b\x00",                   "pextrd [rbx], xmm1, 0"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x01",                   "pextrd [rbx], xmm1, 1"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x02",                   "pextrd [rbx], xmm1, 2"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x03",                   "pextrd [rbx], xmm1, 3"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x04",                   "pextrd [rbx], xmm1, 4"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x05",                   "pextrd [rbx], xmm1, 5"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x06",                   "pextrd [rbx], xmm1, 6"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x07",                   "pextrd [rbx], xmm1, 7"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x08",                   "pextrd [rbx], xmm1, 8"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x09",                   "pextrd [rbx], xmm1, 9"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x0a",                   "pextrd [rbx], xmm1, 10"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x0b",                   "pextrd [rbx], xmm1, 11"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x0c",                   "pextrd [rbx], xmm1, 12"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x0d",                   "pextrd [rbx], xmm1, 13"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x0e",                   "pextrd [rbx], xmm1, 14"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x0f",                   "pextrd [rbx], xmm1, 15"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x10",                   "pextrd [rbx], xmm1, 16"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x11",                   "pextrd [rbx], xmm1, 17"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x12",                   "pextrd [rbx], xmm1, 18"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x13",                   "pextrd [rbx], xmm1, 19"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x14",                   "pextrd [rbx], xmm1, 20"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x15",                   "pextrd [rbx], xmm1, 21"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x16",                   "pextrd [rbx], xmm1, 22"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x17",                   "pextrd [rbx], xmm1, 23"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x18",                   "pextrd [rbx], xmm1, 24"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x19",                   "pextrd [rbx], xmm1, 25"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x1a",                   "pextrd [rbx], xmm1, 26"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x1b",                   "pextrd [rbx], xmm1, 27"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x1c",                   "pextrd [rbx], xmm1, 28"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x1d",                   "pextrd [rbx], xmm1, 29"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x1e",                   "pextrd [rbx], xmm1, 30"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x1f",                   "pextrd [rbx], xmm1, 31"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x20",                   "pextrd [rbx], xmm1, 32"),
    (None, [], b"\x66\x0f\x3a\x16\x0b\x21",                   "pextrd [rbx], xmm1, 33"),

    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x00",               "pextrq rax, xmm1, 0"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x01",               "pextrq rax, xmm1, 1"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x02",               "pextrq rax, xmm1, 2"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x03",               "pextrq rax, xmm1, 3"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x04",               "pextrq rax, xmm1, 4"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x05",               "pextrq rax, xmm1, 5"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x06",               "pextrq rax, xmm1, 6"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x07",               "pextrq rax, xmm1, 7"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x08",               "pextrq rax, xmm1, 8"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x09",               "pextrq rax, xmm1, 9"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x0a",               "pextrq rax, xmm1, 10"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x0b",               "pextrq rax, xmm1, 11"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x0c",               "pextrq rax, xmm1, 12"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x0d",               "pextrq rax, xmm1, 13"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x0e",               "pextrq rax, xmm1, 14"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x0f",               "pextrq rax, xmm1, 15"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x10",               "pextrq rax, xmm1, 16"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x11",               "pextrq rax, xmm1, 17"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x12",               "pextrq rax, xmm1, 18"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x13",               "pextrq rax, xmm1, 19"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x14",               "pextrq rax, xmm1, 20"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x15",               "pextrq rax, xmm1, 21"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x16",               "pextrq rax, xmm1, 22"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x17",               "pextrq rax, xmm1, 23"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x18",               "pextrq rax, xmm1, 24"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x19",               "pextrq rax, xmm1, 25"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x1a",               "pextrq rax, xmm1, 26"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x1b",               "pextrq rax, xmm1, 27"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x1c",               "pextrq rax, xmm1, 28"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x1d",               "pextrq rax, xmm1, 29"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x1e",               "pextrq rax, xmm1, 30"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x1f",               "pextrq rax, xmm1, 31"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x20",               "pextrq rax, xmm1, 32"),
    (None, [], b"\x66\x48\x0f\x3a\x16\xc8\x21",               "pextrq rax, xmm1, 33"),

    (None, [], b"\x66\x0f\xc5\xc1\x00",                       "pextrw eax, xmm1, 0"),
    (None, [], b"\x66\x0f\xc5\xc1\x01",                       "pextrw eax, xmm1, 1"),
    (None, [], b"\x66\x0f\xc5\xc1\x02",                       "pextrw eax, xmm1, 2"),
    (None, [], b"\x66\x0f\xc5\xc1\x03",                       "pextrw eax, xmm1, 3"),
    (None, [], b"\x66\x0f\xc5\xc1\x04",                       "pextrw eax, xmm1, 4"),
    (None, [], b"\x66\x0f\xc5\xc1\x05",                       "pextrw eax, xmm1, 5"),
    (None, [], b"\x66\x0f\xc5\xc1\x06",                       "pextrw eax, xmm1, 6"),
    (None, [], b"\x66\x0f\xc5\xc1\x07",                       "pextrw eax, xmm1, 7"),
    (None, [], b"\x66\x0f\xc5\xc1\x08",                       "pextrw eax, xmm1, 8"),
    (None, [], b"\x66\x0f\xc5\xc1\x09",                       "pextrw eax, xmm1, 9"),
    (None, [], b"\x66\x0f\xc5\xc1\x0a",                       "pextrw eax, xmm1, 10"),
    (None, [], b"\x66\x0f\xc5\xc1\x0b",                       "pextrw eax, xmm1, 11"),
    (None, [], b"\x66\x0f\xc5\xc1\x0c",                       "pextrw eax, xmm1, 12"),
    (None, [], b"\x66\x0f\xc5\xc1\x0d",                       "pextrw eax, xmm1, 13"),
    (None, [], b"\x66\x0f\xc5\xc1\x0e",                       "pextrw eax, xmm1, 14"),
    (None, [], b"\x66\x0f\xc5\xc1\x0f",                       "pextrw eax, xmm1, 15"),
    (None, [], b"\x66\x0f\xc5\xc1\x10",                       "pextrw eax, xmm1, 16"),
    (None, [], b"\x66\x0f\xc5\xc1\x11",                       "pextrw eax, xmm1, 17"),
    (None, [], b"\x66\x0f\xc5\xc1\x12",                       "pextrw eax, xmm1, 18"),
    (None, [], b"\x66\x0f\xc5\xc1\x13",                       "pextrw eax, xmm1, 19"),
    (None, [], b"\x66\x0f\xc5\xc1\x14",                       "pextrw eax, xmm1, 20"),
    (None, [], b"\x66\x0f\xc5\xc1\x15",                       "pextrw eax, xmm1, 21"),
    (None, [], b"\x66\x0f\xc5\xc1\x16",                       "pextrw eax, xmm1, 22"),
    (None, [], b"\x66\x0f\xc5\xc1\x17",                       "pextrw eax, xmm1, 23"),
    (None, [], b"\x66\x0f\xc5\xc1\x18",                       "pextrw eax, xmm1, 24"),
    (None, [], b"\x66\x0f\xc5\xc1\x19",                       "pextrw eax, xmm1, 25"),
    (None, [], b"\x66\x0f\xc5\xc1\x1a",                       "pextrw eax, xmm1, 26"),
    (None, [], b"\x66\x0f\xc5\xc1\x1b",                       "pextrw eax, xmm1, 27"),
    (None, [], b"\x66\x0f\xc5\xc1\x1c",                       "pextrw eax, xmm1, 28"),
    (None, [], b"\x66\x0f\xc5\xc1\x1d",                       "pextrw eax, xmm1, 29"),
    (None, [], b"\x66\x0f\xc5\xc1\x1e",                       "pextrw eax, xmm1, 30"),
    (None, [], b"\x66\x0f\xc5\xc1\x1f",                       "pextrw eax, xmm1, 31"),
    (None, [], b"\x66\x0f\xc5\xc1\x20",                       "pextrw eax, xmm1, 32"),
    (None, [], b"\x66\x0f\xc5\xc1\x21",                       "pextrw eax, xmm1, 33"),

    (None, [], b"\x0f\xc5\xc1\x00",                           "pextrw eax, mm1, 0"),
    (None, [], b"\x0f\xc5\xc1\x01",                           "pextrw eax, mm1, 1"),
    (None, [], b"\x0f\xc5\xc1\x02",                           "pextrw eax, mm1, 2"),
    (None, [], b"\x0f\xc5\xc1\x03",                           "pextrw eax, mm1, 3"),
    (None, [], b"\x0f\xc5\xc1\x04",                           "pextrw eax, mm1, 4"),
    (None, [], b"\x0f\xc5\xc1\x05",                           "pextrw eax, mm1, 5"),
    (None, [], b"\x0f\xc5\xc1\x06",                           "pextrw eax, mm1, 6"),
    (None, [], b"\x0f\xc5\xc1\x07",                           "pextrw eax, mm1, 7"),
    (None, [], b"\x0f\xc5\xc1\x08",                           "pextrw eax, mm1, 8"),
    (None, [], b"\x0f\xc5\xc1\x09",                           "pextrw eax, mm1, 9"),
    (None, [], b"\x0f\xc5\xc1\x0a",                           "pextrw eax, mm1, 10"),
    (None, [], b"\x0f\xc5\xc1\x0b",                           "pextrw eax, mm1, 11"),
    (None, [], b"\x0f\xc5\xc1\x0c",                           "pextrw eax, mm1, 12"),
    (None, [], b"\x0f\xc5\xc1\x0d",                           "pextrw eax, mm1, 13"),
    (None, [], b"\x0f\xc5\xc1\x0e",                           "pextrw eax, mm1, 14"),
    (None, [], b"\x0f\xc5\xc1\x0f",                           "pextrw eax, mm1, 15"),
    (None, [], b"\x0f\xc5\xc1\x10",                           "pextrw eax, mm1, 16"),
    (None, [], b"\x0f\xc5\xc1\x11",                           "pextrw eax, mm1, 17"),
    (None, [], b"\x0f\xc5\xc1\x12",                           "pextrw eax, mm1, 18"),
    (None, [], b"\x0f\xc5\xc1\x13",                           "pextrw eax, mm1, 19"),
    (None, [], b"\x0f\xc5\xc1\x14",                           "pextrw eax, mm1, 20"),
    (None, [], b"\x0f\xc5\xc1\x15",                           "pextrw eax, mm1, 21"),
    (None, [], b"\x0f\xc5\xc1\x16",                           "pextrw eax, mm1, 22"),
    (None, [], b"\x0f\xc5\xc1\x17",                           "pextrw eax, mm1, 23"),
    (None, [], b"\x0f\xc5\xc1\x18",                           "pextrw eax, mm1, 24"),
    (None, [], b"\x0f\xc5\xc1\x19",                           "pextrw eax, mm1, 25"),
    (None, [], b"\x0f\xc5\xc1\x1a",                           "pextrw eax, mm1, 26"),
    (None, [], b"\x0f\xc5\xc1\x1b",                           "pextrw eax, mm1, 27"),
    (None, [], b"\x0f\xc5\xc1\x1c",                           "pextrw eax, mm1, 28"),
    (None, [], b"\x0f\xc5\xc1\x1d",                           "pextrw eax, mm1, 29"),
    (None, [], b"\x0f\xc5\xc1\x1e",                           "pextrw eax, mm1, 30"),
    (None, [], b"\x0f\xc5\xc1\x1f",                           "pextrw eax, mm1, 31"),
    (None, [], b"\x0f\xc5\xc1\x20",                           "pextrw eax, mm1, 32"),
    (None, [], b"\x0f\xc5\xc1\x21",                           "pextrw eax, mm1, 33"),

    (None, [], b"\xc4\xe3\x79\x14\xc8\x00",                   "vpextrb eax, xmm1, 0"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x01",                   "vpextrb eax, xmm1, 1"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x02",                   "vpextrb eax, xmm1, 2"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x03",                   "vpextrb eax, xmm1, 3"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x04",                   "vpextrb eax, xmm1, 4"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x05",                   "vpextrb eax, xmm1, 5"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x06",                   "vpextrb eax, xmm1, 6"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x07",                   "vpextrb eax, xmm1, 7"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x08",                   "vpextrb eax, xmm1, 8"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x09",                   "vpextrb eax, xmm1, 9"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x0a",                   "vpextrb eax, xmm1, 10"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x0b",                   "vpextrb eax, xmm1, 11"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x0c",                   "vpextrb eax, xmm1, 12"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x0d",                   "vpextrb eax, xmm1, 13"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x0e",                   "vpextrb eax, xmm1, 14"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x0f",                   "vpextrb eax, xmm1, 15"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x10",                   "vpextrb eax, xmm1, 16"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x11",                   "vpextrb eax, xmm1, 17"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x12",                   "vpextrb eax, xmm1, 18"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x13",                   "vpextrb eax, xmm1, 19"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x14",                   "vpextrb eax, xmm1, 20"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x15",                   "vpextrb eax, xmm1, 21"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x16",                   "vpextrb eax, xmm1, 22"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x17",                   "vpextrb eax, xmm1, 23"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x18",                   "vpextrb eax, xmm1, 24"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x19",                   "vpextrb eax, xmm1, 25"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x1a",                   "vpextrb eax, xmm1, 26"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x1b",                   "vpextrb eax, xmm1, 27"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x1c",                   "vpextrb eax, xmm1, 28"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x1d",                   "vpextrb eax, xmm1, 29"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x1e",                   "vpextrb eax, xmm1, 30"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x1f",                   "vpextrb eax, xmm1, 31"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x20",                   "vpextrb eax, xmm1, 32"),
    (None, [], b"\xc4\xe3\x79\x14\xc8\x21",                   "vpextrb eax, xmm1, 33"),

    (None, [], b"\xc4\xe3\x79\x16\xc8\x00",                   "vpextrd eax, xmm1, 0"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x01",                   "vpextrd eax, xmm1, 1"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x02",                   "vpextrd eax, xmm1, 2"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x03",                   "vpextrd eax, xmm1, 3"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x04",                   "vpextrd eax, xmm1, 4"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x05",                   "vpextrd eax, xmm1, 5"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x06",                   "vpextrd eax, xmm1, 6"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x07",                   "vpextrd eax, xmm1, 7"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x08",                   "vpextrd eax, xmm1, 8"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x09",                   "vpextrd eax, xmm1, 9"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x0a",                   "vpextrd eax, xmm1, 10"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x0b",                   "vpextrd eax, xmm1, 11"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x0c",                   "vpextrd eax, xmm1, 12"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x0d",                   "vpextrd eax, xmm1, 13"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x0e",                   "vpextrd eax, xmm1, 14"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x0f",                   "vpextrd eax, xmm1, 15"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x10",                   "vpextrd eax, xmm1, 16"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x11",                   "vpextrd eax, xmm1, 17"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x12",                   "vpextrd eax, xmm1, 18"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x13",                   "vpextrd eax, xmm1, 19"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x14",                   "vpextrd eax, xmm1, 20"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x15",                   "vpextrd eax, xmm1, 21"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x16",                   "vpextrd eax, xmm1, 22"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x17",                   "vpextrd eax, xmm1, 23"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x18",                   "vpextrd eax, xmm1, 24"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x19",                   "vpextrd eax, xmm1, 25"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x1a",                   "vpextrd eax, xmm1, 26"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x1b",                   "vpextrd eax, xmm1, 27"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x1c",                   "vpextrd eax, xmm1, 28"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x1d",                   "vpextrd eax, xmm1, 29"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x1e",                   "vpextrd eax, xmm1, 30"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x1f",                   "vpextrd eax, xmm1, 31"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x20",                   "vpextrd eax, xmm1, 32"),
    (None, [], b"\xc4\xe3\x79\x16\xc8\x21",                   "vpextrd eax, xmm1, 33"),

    (None, [], b"\xc4\xe3\xf9\x16\xc8\x00",                   "vpextrq rax, xmm1, 0"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x01",                   "vpextrq rax, xmm1, 1"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x02",                   "vpextrq rax, xmm1, 2"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x03",                   "vpextrq rax, xmm1, 3"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x04",                   "vpextrq rax, xmm1, 4"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x05",                   "vpextrq rax, xmm1, 5"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x06",                   "vpextrq rax, xmm1, 6"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x07",                   "vpextrq rax, xmm1, 7"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x08",                   "vpextrq rax, xmm1, 8"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x09",                   "vpextrq rax, xmm1, 9"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x0a",                   "vpextrq rax, xmm1, 10"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x0b",                   "vpextrq rax, xmm1, 11"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x0c",                   "vpextrq rax, xmm1, 12"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x0d",                   "vpextrq rax, xmm1, 13"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x0e",                   "vpextrq rax, xmm1, 14"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x0f",                   "vpextrq rax, xmm1, 15"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x10",                   "vpextrq rax, xmm1, 16"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x11",                   "vpextrq rax, xmm1, 17"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x12",                   "vpextrq rax, xmm1, 18"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x13",                   "vpextrq rax, xmm1, 19"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x14",                   "vpextrq rax, xmm1, 20"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x15",                   "vpextrq rax, xmm1, 21"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x16",                   "vpextrq rax, xmm1, 22"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x17",                   "vpextrq rax, xmm1, 23"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x18",                   "vpextrq rax, xmm1, 24"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x19",                   "vpextrq rax, xmm1, 25"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x1a",                   "vpextrq rax, xmm1, 26"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x1b",                   "vpextrq rax, xmm1, 27"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x1c",                   "vpextrq rax, xmm1, 28"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x1d",                   "vpextrq rax, xmm1, 29"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x1e",                   "vpextrq rax, xmm1, 30"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x1f",                   "vpextrq rax, xmm1, 31"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x20",                   "vpextrq rax, xmm1, 32"),
    (None, [], b"\xc4\xe3\xf9\x16\xc8\x21",                   "vpextrq rax, xmm1, 33"),

    (None, [], b"\xc5\xf9\xc5\xc1\x00",                       "vpextrw eax, xmm1, 0"),
    (None, [], b"\xc5\xf9\xc5\xc1\x01",                       "vpextrw eax, xmm1, 1"),
    (None, [], b"\xc5\xf9\xc5\xc1\x02",                       "vpextrw eax, xmm1, 2"),
    (None, [], b"\xc5\xf9\xc5\xc1\x03",                       "vpextrw eax, xmm1, 3"),
    (None, [], b"\xc5\xf9\xc5\xc1\x04",                       "vpextrw eax, xmm1, 4"),
    (None, [], b"\xc5\xf9\xc5\xc1\x05",                       "vpextrw eax, xmm1, 5"),
    (None, [], b"\xc5\xf9\xc5\xc1\x06",                       "vpextrw eax, xmm1, 6"),
    (None, [], b"\xc5\xf9\xc5\xc1\x07",                       "vpextrw eax, xmm1, 7"),
    (None, [], b"\xc5\xf9\xc5\xc1\x08",                       "vpextrw eax, xmm1, 8"),
    (None, [], b"\xc5\xf9\xc5\xc1\x09",                       "vpextrw eax, xmm1, 9"),
    (None, [], b"\xc5\xf9\xc5\xc1\x0a",                       "vpextrw eax, xmm1, 10"),
    (None, [], b"\xc5\xf9\xc5\xc1\x0b",                       "vpextrw eax, xmm1, 11"),
    (None, [], b"\xc5\xf9\xc5\xc1\x0c",                       "vpextrw eax, xmm1, 12"),
    (None, [], b"\xc5\xf9\xc5\xc1\x0d",                       "vpextrw eax, xmm1, 13"),
    (None, [], b"\xc5\xf9\xc5\xc1\x0e",                       "vpextrw eax, xmm1, 14"),
    (None, [], b"\xc5\xf9\xc5\xc1\x0f",                       "vpextrw eax, xmm1, 15"),
    (None, [], b"\xc5\xf9\xc5\xc1\x10",                       "vpextrw eax, xmm1, 16"),
    (None, [], b"\xc5\xf9\xc5\xc1\x11",                       "vpextrw eax, xmm1, 17"),
    (None, [], b"\xc5\xf9\xc5\xc1\x12",                       "vpextrw eax, xmm1, 18"),
    (None, [], b"\xc5\xf9\xc5\xc1\x13",                       "vpextrw eax, xmm1, 19"),
    (None, [], b"\xc5\xf9\xc5\xc1\x14",                       "vpextrw eax, xmm1, 20"),
    (None, [], b"\xc5\xf9\xc5\xc1\x15",                       "vpextrw eax, xmm1, 21"),
    (None, [], b"\xc5\xf9\xc5\xc1\x16",                       "vpextrw eax, xmm1, 22"),
    (None, [], b"\xc5\xf9\xc5\xc1\x17",                       "vpextrw eax, xmm1, 23"),
    (None, [], b"\xc5\xf9\xc5\xc1\x18",                       "vpextrw eax, xmm1, 24"),
    (None, [], b"\xc5\xf9\xc5\xc1\x19",                       "vpextrw eax, xmm1, 25"),
    (None, [], b"\xc5\xf9\xc5\xc1\x1a",                       "vpextrw eax, xmm1, 26"),
    (None, [], b"\xc5\xf9\xc5\xc1\x1b",                       "vpextrw eax, xmm1, 27"),
    (None, [], b"\xc5\xf9\xc5\xc1\x1c",                       "vpextrw eax, xmm1, 28"),
    (None, [], b"\xc5\xf9\xc5\xc1\x1d",                       "vpextrw eax, xmm1, 29"),
    (None, [], b"\xc5\xf9\xc5\xc1\x1e",                       "vpextrw eax, xmm1, 30"),
    (None, [], b"\xc5\xf9\xc5\xc1\x1f",                       "vpextrw eax, xmm1, 31"),
    (None, [], b"\xc5\xf9\xc5\xc1\x20",                       "vpextrw eax, xmm1, 32"),
    (None, [], b"\xc5\xf9\xc5\xc1\x21",                       "vpextrw eax, xmm1, 33"),

    (None, [], b"\x48\xb8\xaf\xbe\xad\xde\xaf\xbe\xad\xde",   "mov rax, 0xdeadbeafdeadbeaf"),
    (None, [], b"\x48\xc7\xc3\x00\x00\x20\x00",               "mov rbx, 0x300010"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x00",                   "pinsrb xmm1, eax, 0"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x01",                   "pinsrb xmm1, eax, 1"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x02",                   "pinsrb xmm1, eax, 2"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x03",                   "pinsrb xmm1, eax, 3"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x04",                   "pinsrb xmm1, eax, 4"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x05",                   "pinsrb xmm1, eax, 5"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x06",                   "pinsrb xmm1, eax, 6"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x07",                   "pinsrb xmm1, eax, 7"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x08",                   "pinsrb xmm1, eax, 8"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x09",                   "pinsrb xmm1, eax, 9"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x0a",                   "pinsrb xmm1, eax, 10"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x0b",                   "pinsrb xmm1, eax, 11"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x0c",                   "pinsrb xmm1, eax, 12"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x0d",                   "pinsrb xmm1, eax, 13"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x0e",                   "pinsrb xmm1, eax, 14"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x0f",                   "pinsrb xmm1, eax, 15"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x10",                   "pinsrb xmm1, eax, 16"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x11",                   "pinsrb xmm1, eax, 17"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x12",                   "pinsrb xmm1, eax, 18"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x13",                   "pinsrb xmm1, eax, 19"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x14",                   "pinsrb xmm1, eax, 20"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x15",                   "pinsrb xmm1, eax, 21"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x16",                   "pinsrb xmm1, eax, 22"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x17",                   "pinsrb xmm1, eax, 23"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x18",                   "pinsrb xmm1, eax, 24"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x19",                   "pinsrb xmm1, eax, 25"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x1a",                   "pinsrb xmm1, eax, 26"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x1b",                   "pinsrb xmm1, eax, 27"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x1c",                   "pinsrb xmm1, eax, 28"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x1d",                   "pinsrb xmm1, eax, 29"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x1e",                   "pinsrb xmm1, eax, 30"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x1f",                   "pinsrb xmm1, eax, 31"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x20",                   "pinsrb xmm1, eax, 32"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x20\xc8\x21",                   "pinsrb xmm1, eax, 33"),


    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x00",                   "pinsrd xmm1, eax, 0"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x01",                   "pinsrd xmm1, eax, 1"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x02",                   "pinsrd xmm1, eax, 2"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x03",                   "pinsrd xmm1, eax, 3"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x04",                   "pinsrd xmm1, eax, 4"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x05",                   "pinsrd xmm1, eax, 5"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x06",                   "pinsrd xmm1, eax, 6"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x07",                   "pinsrd xmm1, eax, 7"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x08",                   "pinsrd xmm1, eax, 8"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x09",                   "pinsrd xmm1, eax, 9"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x0a",                   "pinsrd xmm1, eax, 10"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x0b",                   "pinsrd xmm1, eax, 11"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x0c",                   "pinsrd xmm1, eax, 12"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x0d",                   "pinsrd xmm1, eax, 13"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x0e",                   "pinsrd xmm1, eax, 14"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x0f",                   "pinsrd xmm1, eax, 15"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x10",                   "pinsrd xmm1, eax, 16"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x11",                   "pinsrd xmm1, eax, 17"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x12",                   "pinsrd xmm1, eax, 18"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x13",                   "pinsrd xmm1, eax, 19"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x14",                   "pinsrd xmm1, eax, 20"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x15",                   "pinsrd xmm1, eax, 21"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x16",                   "pinsrd xmm1, eax, 22"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x17",                   "pinsrd xmm1, eax, 23"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x18",                   "pinsrd xmm1, eax, 24"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x19",                   "pinsrd xmm1, eax, 25"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x1a",                   "pinsrd xmm1, eax, 26"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x1b",                   "pinsrd xmm1, eax, 27"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x1c",                   "pinsrd xmm1, eax, 28"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x1d",                   "pinsrd xmm1, eax, 29"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x1e",                   "pinsrd xmm1, eax, 30"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x1f",                   "pinsrd xmm1, eax, 31"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x20",                   "pinsrd xmm1, eax, 32"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\x3a\x22\xc8\x21",                   "pinsrd xmm1, eax, 33"),

    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x00",               "pinsrq xmm1, rax, 0"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x01",               "pinsrq xmm1, rax, 1"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x02",               "pinsrq xmm1, rax, 2"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x03",               "pinsrq xmm1, rax, 3"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x04",               "pinsrq xmm1, rax, 4"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x05",               "pinsrq xmm1, rax, 5"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x06",               "pinsrq xmm1, rax, 6"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x07",               "pinsrq xmm1, rax, 7"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x08",               "pinsrq xmm1, rax, 8"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x09",               "pinsrq xmm1, rax, 9"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x0a",               "pinsrq xmm1, rax, 10"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x0b",               "pinsrq xmm1, rax, 11"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x0c",               "pinsrq xmm1, rax, 12"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x0d",               "pinsrq xmm1, rax, 13"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x0e",               "pinsrq xmm1, rax, 14"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x0f",               "pinsrq xmm1, rax, 15"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x10",               "pinsrq xmm1, rax, 16"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x11",               "pinsrq xmm1, rax, 17"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x12",               "pinsrq xmm1, rax, 18"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x13",               "pinsrq xmm1, rax, 19"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x14",               "pinsrq xmm1, rax, 20"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x15",               "pinsrq xmm1, rax, 21"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x16",               "pinsrq xmm1, rax, 22"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x17",               "pinsrq xmm1, rax, 23"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x18",               "pinsrq xmm1, rax, 24"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x19",               "pinsrq xmm1, rax, 25"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x1a",               "pinsrq xmm1, rax, 26"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x1b",               "pinsrq xmm1, rax, 27"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x1c",               "pinsrq xmm1, rax, 28"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x1d",               "pinsrq xmm1, rax, 29"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x1e",               "pinsrq xmm1, rax, 30"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x1f",               "pinsrq xmm1, rax, 31"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x20",               "pinsrq xmm1, rax, 32"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x48\x0f\x3a\x22\xc8\x21",               "pinsrq xmm1, rax, 33"),

    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x00",                       "pinsrw xmm1, eax, 0"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x01",                       "pinsrw xmm1, eax, 1"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x02",                       "pinsrw xmm1, eax, 2"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x03",                       "pinsrw xmm1, eax, 3"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x04",                       "pinsrw xmm1, eax, 4"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x05",                       "pinsrw xmm1, eax, 5"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x06",                       "pinsrw xmm1, eax, 6"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x07",                       "pinsrw xmm1, eax, 7"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x08",                       "pinsrw xmm1, eax, 8"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x09",                       "pinsrw xmm1, eax, 9"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x0a",                       "pinsrw xmm1, eax, 10"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x0b",                       "pinsrw xmm1, eax, 11"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x0c",                       "pinsrw xmm1, eax, 12"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x0d",                       "pinsrw xmm1, eax, 13"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x0e",                       "pinsrw xmm1, eax, 14"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x0f",                       "pinsrw xmm1, eax, 15"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x10",                       "pinsrw xmm1, eax, 16"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x11",                       "pinsrw xmm1, eax, 17"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x12",                       "pinsrw xmm1, eax, 18"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x13",                       "pinsrw xmm1, eax, 19"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x14",                       "pinsrw xmm1, eax, 20"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x15",                       "pinsrw xmm1, eax, 21"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x16",                       "pinsrw xmm1, eax, 22"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x17",                       "pinsrw xmm1, eax, 23"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x18",                       "pinsrw xmm1, eax, 24"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x19",                       "pinsrw xmm1, eax, 25"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x1a",                       "pinsrw xmm1, eax, 26"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x1b",                       "pinsrw xmm1, eax, 27"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x1c",                       "pinsrw xmm1, eax, 28"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x1d",                       "pinsrw xmm1, eax, 29"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x1e",                       "pinsrw xmm1, eax, 30"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x1f",                       "pinsrw xmm1, eax, 31"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x20",                       "pinsrw xmm1, eax, 32"),
    (None, [], b"\x0f\x28\x0b",                               "movaps xmm1, [rbx]"),
    (None, [], b"\x66\x0f\xc4\xc8\x21",                       "pinsrw xmm1, eax, 33"),

    ({'eflags':2}, [], b"\x90",                               "nop"),
    (None, [], b"\x48\xc7\xc0\x00\x00\x00\x00",               "mov rax, 0x0"),
    (None, [], b"\x48\xc7\xc3\x00\x00\x00\x00",               "mov rbx, 0x0"),
    (None, [], b"\xf3\x48\x0f\xbd\xd8",                       "lzcnt rbx, rax"),
    (None, [], b"\x48\xc7\xc0\x00\x00\x00\x00",               "mov rax, 0x0"),
    (None, [], b"\x48\xc7\xc3\x01\x00\x00\x00",               "mov rbx, 0x1"),
    (None, [], b"\xf3\x48\x0f\xbd\xd8",                       "lzcnt rbx, rax"),
    (None, [], b"\x48\xc7\xc0\x01\x00\x00\x00",               "mov rax, 0x1"),
    (None, [], b"\x48\xc7\xc3\x00\x00\x00\x00",               "mov rbx, 0x0"),
    (None, [], b"\xf3\x48\x0f\xbd\xd8",                       "lzcnt rbx, rax"),
    (None, [], b"\x48\xc7\xc0\x02\x00\x00\x00",               "mov rax, 0x2"),
    (None, [], b"\xf3\x48\x0f\xbd\xd8",                       "lzcnt rbx, rax"),
    (None, [], b"\x48\xc7\xc0\x40\x00\x00\x00",               "mov rax, 0x40"),
    (None, [], b"\xf3\x48\x0f\xbd\xd8",                       "lzcnt rbx, rax"),
    (None, [], b"\x48\xc7\xc0\x00\x10\x00\x00",               "mov rax, 0x1000"),
    (None, [], b"\xf3\x48\x0f\xbd\xd8",                       "lzcnt rbx, rax"),
    (None, [], b"\x66\xf3\x0f\xbd\xd8",                       "lzcnt bx, ax"),
    (None, [], b"\x48\xc7\xc0\x00\x00\x00\x00",               "mov rax, 0x0"),
    (None, [], b"\xf3\x48\x0f\xbd\xd8",                       "lzcnt rbx, rax"),
    (None, [], b"\x48\xb8\x00\x00\x00\x00\x00\x00\x00\x80",   "movabs rax, 0x8000000000000000"),
    (None, [], b"\xf3\x48\x0f\xbd\xd8",                       "lzcnt rbx, rax"),
    (None, [], b"\x48\xc7\xc0\xff\xff\xff\xff",               "mov rax, 0xffffffffffffffff"),
    (None, [], b"\x48\xc7\xc3\x00\x00\x00\x00",               "mov rbx, 0x0"),
    (None, [], b"\xf3\x48\x0f\xbd\xd8",                       "lzcnt rbx, rax"),

    (None, [], b"\x48\xc7\xc0\x00\x00\x00\x00",               "mov rax, 0x0"),
    (None, [], b"\x48\xc7\xc3\x00\x00\x00\x00",               "mov rbx, 0x0"),
    (None, [], b"\xf3\x0f\xbd\xd8",                           "lzcnt ebx, eax"),
    (None, [], b"\x48\xc7\xc0\x00\x00\x00\x00",               "mov rax, 0x0"),
    (None, [], b"\x48\xc7\xc3\x01\x00\x00\x00",               "mov rbx, 0x1"),
    (None, [], b"\xf3\x0f\xbd\xd8",                           "lzcnt ebx, eax"),
    (None, [], b"\x48\xc7\xc0\x01\x00\x00\x00",               "mov rax, 0x1"),
    (None, [], b"\x48\xc7\xc3\x00\x00\x00\x00",               "mov rbx, 0x0"),
    (None, [], b"\xf3\x0f\xbd\xd8",                           "lzcnt ebx, eax"),
    (None, [], b"\x48\xc7\xc0\x02\x00\x00\x00",               "mov rax, 0x2"),
    (None, [], b"\xf3\x0f\xbd\xd8",                           "lzcnt ebx, eax"),
    (None, [], b"\x48\xc7\xc0\x40\x00\x00\x00",               "mov rax, 0x40"),
    (None, [], b"\xf3\x0f\xbd\xd8",                           "lzcnt ebx, eax"),
    (None, [], b"\x48\xc7\xc0\x00\x10\x00\x00",               "mov rax, 0x1000"),
    (None, [], b"\xf3\x0f\xbd\xd8",                           "lzcnt ebx, eax"),
    (None, [], b"\x66\xf3\x0f\xbd\xd8",                       "lzcnt bx, ax"),
    (None, [], b"\x48\xc7\xc0\x00\x00\x00\x00",               "mov rax, 0x0"),
    (None, [], b"\xf3\x0f\xbd\xd8",                           "lzcnt ebx, eax"),
    (None, [], b"\x48\xb8\x00\x00\x00\x00\x00\x00\x00\x80",   "movabs rax, 0x8000000000000000"),
    (None, [], b"\xf3\x0f\xbd\xd8",                           "lzcnt ebx, eax"),
    (None, [], b"\x48\xc7\xc0\xff\xff\xff\xff",               "mov rax, 0xffffffffffffffff"),
    (None, [], b"\x48\xc7\xc3\x00\x00\x00\x00",               "mov rbx, 0x0"),
    (None, [], b"\xf3\x0f\xbd\xd8",                           "lzcnt ebx, eax"),

    (None, [], b"\x48\xc7\xc0\x00\x00\x00\x00",               "mov rax, 0x0"),
    (None, [], b"\x48\xc7\xc3\x00\x00\x00\x00",               "mov rbx, 0x0"),
    (None, [], b"\xf3\x48\x0f\xbc\xd8",                       "tzcnt rbx, rax"),
    (None, [], b"\x48\xc7\xc0\x00\x00\x00\x00",               "mov rax, 0x0"),
    (None, [], b"\x48\xc7\xc3\x01\x00\x00\x00",               "mov rbx, 0x1"),
    (None, [], b"\xf3\x48\x0f\xbc\xd8",                       "tzcnt rbx, rax"),
    (None, [], b"\x48\xc7\xc0\x01\x00\x00\x00",               "mov rax, 0x1"),
    (None, [], b"\x48\xc7\xc3\x00\x00\x00\x00",               "mov rbx, 0x0"),
    (None, [], b"\xf3\x48\x0f\xbc\xd8",                       "tzcnt rbx, rax"),
    (None, [], b"\x48\xc7\xc0\x02\x00\x00\x00",               "mov rax, 0x2"),
    (None, [], b"\xf3\x48\x0f\xbc\xd8",                       "tzcnt rbx, rax"),
    (None, [], b"\x48\xc7\xc0\x40\x00\x00\x00",               "mov rax, 0x40"),
    (None, [], b"\xf3\x48\x0f\xbc\xd8",                       "tzcnt rbx, rax"),
    (None, [], b"\x48\xc7\xc0\x00\x10\x00\x00",               "mov rax, 0x1000"),
    (None, [], b"\x66\xf3\x0f\xbc\xd8",                       "tzcnt bx, ax"),
    (None, [], b"\x48\xc7\xc0\x00\x00\x00\x00",               "mov rax, 0x0"),
    (None, [], b"\xf3\x48\x0f\xbc\xd8",                       "tzcnt rbx, rax"),
    (None, [], b"\x48\xb8\x00\x00\x00\x00\x00\x00\x00\x80",   "movabs rax, 0x8000000000000000"),
    (None, [], b"\xf3\x48\x0f\xbc\xd8",                       "tzcnt rbx, rax"),
    (None, [], b"\x48\xc7\xc0\xff\xff\xff\xff",               "mov rax, 0xffffffffffffffff"),
    (None, [], b"\x48\xc7\xc3\x00\x00\x00\x00",               "mov rbx, 0x0"),
    (None, [], b"\xf3\x48\x0f\xbc\xd8",                       "tzcnt rbx, rax"),

    (None, [], b"\x48\xc7\xc0\x00\x00\x00\x00",               "mov rax, 0x0"),
    (None, [], b"\x48\xc7\xc3\x00\x00\x00\x00",               "mov rbx, 0x0"),
    (None, [], b"\xf3\x0f\xbc\xd8",                           "tzcnt ebx, eax"),
    (None, [], b"\x48\xc7\xc0\x00\x00\x00\x00",               "mov rax, 0x0"),
    (None, [], b"\x48\xc7\xc3\x01\x00\x00\x00",               "mov rbx, 0x1"),
    (None, [], b"\xf3\x0f\xbc\xd8",                           "tzcnt ebx, eax"),
    (None, [], b"\x48\xc7\xc0\x01\x00\x00\x00",               "mov rax, 0x1"),
    (None, [], b"\x48\xc7\xc3\x00\x00\x00\x00",               "mov rbx, 0x0"),
    (None, [], b"\xf3\x0f\xbc\xd8",                           "tzcnt ebx, eax"),
    (None, [], b"\x48\xc7\xc0\x02\x00\x00\x00",               "mov rax, 0x2"),
    (None, [], b"\xf3\x0f\xbc\xd8",                           "tzcnt ebx, eax"),
    (None, [], b"\x48\xc7\xc0\x40\x00\x00\x00",               "mov rax, 0x40"),
    (None, [], b"\xf3\x0f\xbc\xd8",                           "tzcnt ebx, eax"),
    (None, [], b"\x48\xc7\xc0\x00\x10\x00\x00",               "mov rax, 0x1000"),
    (None, [], b"\x66\xf3\x0f\xbc\xd8",                       "tzcnt bx, ax"),
    (None, [], b"\x48\xc7\xc0\x00\x00\x00\x00",               "mov rax, 0x0"),
    (None, [], b"\xf3\x0f\xbc\xd8",                           "tzcnt ebx, eax"),
    (None, [], b"\x48\xb8\x00\x00\x00\x00\x00\x00\x00\x80",   "movabs rax, 0x8000000000000000"),
    (None, [], b"\xf3\x0f\xbc\xd8",                           "tzcnt ebx, eax"),
    (None, [], b"\x48\xc7\xc0\xff\xff\xff\xff",               "mov rax, 0xffffffffffffffff"),
    (None, [], b"\x48\xc7\xc3\x00\x00\x00\x00",               "mov rbx, 0x0"),
    (None, [], b"\xf3\x0f\xbc\xd8",                           "tzcnt ebx, eax"),

    (None, [], b"\x48\xB8\x11\x11\x11\x11\x11\x11\x11\x11",   "movabs rax, 1111111111111111"),
    (None, [], b"\x66\x48\x0F\x6E\xC0",                       "movq xmm0, rax"),
    (None, [], b"\x66\x48\x0F\x3A\x22\xC0\x01",               "pinsrq xmm0, rax, 1"),
    (None, [], b"\x48\xB8\x22\x22\x22\x22\x22\x22\x22\x22",   "movabs rax, 2222222222222222"),
    (None, [], b"\x66\x48\x0F\x6E\xC8",                       "movq xmm1, rax"),
    (None, [], b"\x66\x48\x0F\x3A\x22\xC8\x01",               "pinsrq xmm1, rax, 1"),
    (None, [], b"\xC5\xF9\xEB\xC1",                           "vpor xmm0, xmm0, xmm1"),

    (None, [], b"\xbb\x10\x00\x30\x00",                       "mov ebx, 0x300010"),
    (None, [], b"\xb8\x20\x00\x30\x00",                       "mov eax, 0x300020"),
    (None, [], b"\xc7\x03\x10\x00\x00\x00",                   "mov [ebx], 0x10"),
    (None, [], b"\x66\x0f\xef\xc0",                           "pxor xmm0, xmm0"),
    (None, [], b"\x66\x0f\xef\xc9",                           "pxor xmm1, xmm1"),
    (None, [], b"\xf3\x0f\x10\xc1",                           "movss xmm1, xmm0"),
    (None, [], b"\xf3\x0f\x11\x03",                           "movss xmm0, [ebx]"),
    (None, [], b"\xf3\x0f\x10\x03",                           "movss [eax], xmm0"),
    (None, [], b"\x48\xB8\xEC\xE3\x96\xE1\x44\x6F\xE9\xBD",   "mov rax, BDE96F44E196E3EC"),
    (None, [], b"\x48\x89\x04\x24",                           "mov qword ptr ss:[rsp], rax"),
    (None, [], b"\x48\xB8\xB2\x7D\xB6\x97\xE7\xB8\x50\xA5",   "mov rax, A550B8E797B67DB2"),
    (None, [], b"\x48\x89\x44\x24\x08",                       "mov qword ptr ss:[rsp+8], rax"),
    (None, [], b"\x48\xB8\x02\x70\xE7\xC5\xF4\x9F\x47\xD8",   "mov rax, D8479FF4C5E77002"),
    (None, [], b"\x48\x89\x44\x24\x10",                       "mov qword ptr ss:[rsp+10], rax"),
    (None, [], b"\x48\xB8\x44\x56\xE0\xA9\x0D\x06\x8B\xC6",   "mov rax, C68B060DA9E05644"),
    (None, [], b"\x48\x89\x44\x24\x18",                       "mov qword ptr ss:[rsp+18], rax"),
    (None, [], b"\xC5\xFD\x6F\x04\x24",                       "vmovdqa ymm0, yword ptr ss:[rsp]"),
    (None, [], b"\x48\xB8\x8D\x8D\xB6\x84\x3C\x1B\x9B\xDC",   "mov rax, DC9B1B3C84B68D8D"),
    (None, [], b"\x48\x89\x04\x24",                           "mov qword ptr ss:[rsp], rax"),
    (None, [], b"\x48\xB8\x92\x11\xD9\xF9\x80\x98\x38\xC0",   "mov rax, C0389880F9D91192"),
    (None, [], b"\x48\x89\x44\x24\x08",                       "mov qword ptr ss:[rsp+8], rax"),
    (None, [], b"\x48\xB8\x6E\x1C\x88\x9A\x83\xF0\x35\xB4",   "mov rax, B435F0839A881C6E"),
    (None, [], b"\x48\x89\x44\x24\x10",                       "mov qword ptr ss:[rsp+10], rax"),
    (None, [], b"\x48\xB8\x20\x56\xE0\xA9\x0D\x06\x8B\xC6",   "mov rax, C68B060DA9E05620"),
    (None, [], b"\x48\x89\x44\x24\x18",                       "mov qword ptr ss:[rsp+18], rax"),
    (None, [], b"\xC5\xFD\x6F\x0C\x24",                       "vmovdqa ymm1, yword ptr ss:[rsp]"),
    (None, [], b"\xC5\xFD\xEF\xC1",                           "vpxor ymm0, ymm0, ymm1"),

    (None, [],              b"\xbb\xd5\x71\x36\x00",          "mov ebx, 0x3671d5"),
    (None, [],              b"\xd1\xc3",                      "rol ebx, 1"),
    (None, [REG.X86_64.OF], b"\xc1\xc3\x02",                  "rol ebx, 2"),
    (None, [REG.X86_64.OF], b"\xc1\xc3\x03",                  "rol ebx, 3"),
    (None, [REG.X86_64.OF], b"\xc1\xc3\x04",                  "rol ebx, 4"),
    (None, [REG.X86_64.OF], b"\xc1\xc3\x05",                  "rol ebx, 5"),
    (None, [REG.X86_64.OF], b"\xc1\xc3\x06",                  "rol ebx, 6"),
    (None, [REG.X86_64.OF], b"\xc1\xc3\x1e",                  "rol ebx, 30"),
    (None, [REG.X86_64.OF], b"\xc1\xc3\x1f",                  "rol ebx, 31"),
    (None, [REG.X86_64.OF], b"\xc1\xc3\x20",                  "rol ebx, 32"),
    (None, [REG.X86_64.OF], b"\xc1\xc3\x21",                  "rol ebx, 33"),
    (None, [],              b"\xbb\x00\x00\x00\x80",          "mov ebx, 0x80000000"),
    (None, [],              b"\xd1\xc3",                      "rol ebx, 1"),
    (None, [],              b"\xbb\x00\x00\x00\x80",          "mov ebx, 0x80000000"),
    (None, [REG.X86_64.OF], b"\xc1\xc3\x02",                  "rol ebx, 2"),
    (None, [],              b"\xbb\x00\x00\x00\x80",          "mov ebx, 0x80000000"),
    (None, [REG.X86_64.OF], b"\xc1\xc3\x03",                  "rol ebx, 3"),

    (None, [],              b"\xbb\xd5\x71\x36\x00",          "mov ebx, 0x3671d5"),
    (None, [],              b"\xd1\xcb",                      "ror ebx, 1"),
    (None, [REG.X86_64.OF], b"\xc1\xcb\x02",                  "ror ebx, 2"),
    (None, [REG.X86_64.OF], b"\xc1\xcb\x03",                  "ror ebx, 3"),
    (None, [REG.X86_64.OF], b"\xc1\xcb\x04",                  "ror ebx, 4"),
    (None, [REG.X86_64.OF], b"\xc1\xcb\x05",                  "ror ebx, 5"),
    (None, [REG.X86_64.OF], b"\xc1\xcb\x06",                  "ror ebx, 6"),
    (None, [REG.X86_64.OF], b"\xc1\xcb\x1e",                  "ror ebx, 30"),
    (None, [REG.X86_64.OF], b"\xc1\xcb\x1f",                  "ror ebx, 31"),
    (None, [REG.X86_64.OF], b"\xc1\xcb\x20",                  "ror ebx, 32"),
    (None, [REG.X86_64.OF], b"\xc1\xcb\x21",                  "ror ebx, 33"),
    (None, [],              b"\xbb\x00\x00\x00\x80",          "mov ebx, 0x80000000"),
    (None, [],              b"\xd1\xcb",                      "ror ebx, 1"),
    (None, [],              b"\xbb\x00\x00\x00\x80",          "mov ebx, 0x80000000"),
    (None, [REG.X86_64.OF], b"\xc1\xcb\x02",                  "ror ebx, 2"),
    (None, [],              b"\xbb\x00\x00\x00\x80",          "mov ebx, 0x80000000"),
    (None, [REG.X86_64.OF], b"\xc1\xcb\x03",                  "ror ebx, 3"),
    (None, [],              b"\xbb\x01\x00\x00\x00",          "mov ebx, 0x00000001"),
    (None, [],              b"\xd1\xcb",                      "ror ebx, 1"),
    (None, [],              b"\xbb\x01\x00\x00\x00",          "mov ebx, 0x00000001"),
    (None, [REG.X86_64.OF], b"\xc1\xcb\x02",                  "ror ebx, 2"),
    (None, [],              b"\xbb\x01\x00\x00\x00",          "mov ebx, 0x00000001"),
    (None, [REG.X86_64.OF], b"\xc1\xcb\x03",                  "ror ebx, 3"),

    (None, [],              b"\xbb\xd5\x71\x36\x00",          "mov ebx, 0x3671d5"),
    (None, [],              b"\xd1\xdb",                      "rcr ebx, 1"),
    (None, [REG.X86_64.OF], b"\xc1\xdb\x02",                  "rcr ebx, 2"),
    (None, [REG.X86_64.OF], b"\xc1\xdb\x03",                  "rcr ebx, 3"),
    (None, [REG.X86_64.OF], b"\xc1\xdb\x04",                  "rcr ebx, 4"),
    (None, [REG.X86_64.OF], b"\xc1\xdb\x05",                  "rcr ebx, 5"),
    (None, [REG.X86_64.OF], b"\xc1\xdb\x06",                  "rcr ebx, 6"),
    (None, [REG.X86_64.OF], b"\xc1\xdb\x1e",                  "rcr ebx, 30"),
    (None, [REG.X86_64.OF], b"\xc1\xdb\x1f",                  "rcr ebx, 31"),
    (None, [REG.X86_64.OF], b"\xc1\xdb\x20",                  "rcr ebx, 32"),
    (None, [REG.X86_64.OF], b"\xc1\xdb\x21",                  "rcr ebx, 33"),
    (None, [],              b"\xbb\x00\x00\x00\x80",          "mov ebx, 0x80000000"),
    (None, [],              b"\xd1\xdb",                      "rcr ebx, 1"),
    (None, [],              b"\xbb\x00\x00\x00\x80",          "mov ebx, 0x80000000"),
    (None, [REG.X86_64.OF], b"\xc1\xdb\x02",                  "rcr ebx, 2"),
    (None, [],              b"\xbb\x00\x00\x00\x80",          "mov ebx, 0x80000000"),
    (None, [REG.X86_64.OF], b"\xc1\xdb\x03",                  "rcr ebx, 3"),
    (None, [],              b"\xbb\x01\x00\x00\x00",          "mov ebx, 0x00000001"),
    (None, [],              b"\xd1\xdb",                      "rcr ebx, 1"),
    (None, [],              b"\xbb\x01\x00\x00\x00",          "mov ebx, 0x00000001"),
    (None, [REG.X86_64.OF], b"\xc1\xdb\x02",                  "rcr ebx, 2"),
    (None, [],              b"\xbb\x01\x00\x00\x00",          "mov ebx, 0x00000001"),
    (None, [REG.X86_64.OF], b"\xc1\xdb\x03",                  "rcr ebx, 3"),

    (None, [],              b"\xbb\xd5\x71\x36\x00",          "mov ebx, 0x3671d5"),
    (None, [],              b"\xd1\xd3",                      "rcl ebx, 1"),
    (None, [REG.X86_64.OF], b"\xc1\xd3\x02",                  "rcl ebx, 2"),
    (None, [REG.X86_64.OF], b"\xc1\xd3\x03",                  "rcl ebx, 3"),
    (None, [REG.X86_64.OF], b"\xc1\xd3\x04",                  "rcl ebx, 4"),
    (None, [REG.X86_64.OF], b"\xc1\xd3\x05",                  "rcl ebx, 5"),
    (None, [REG.X86_64.OF], b"\xc1\xd3\x06",                  "rcl ebx, 6"),
    (None, [REG.X86_64.OF], b"\xc1\xd3\x1e",                  "rcl ebx, 30"),
    (None, [REG.X86_64.OF], b"\xc1\xd3\x1f",                  "rcl ebx, 31"),
    (None, [REG.X86_64.OF], b"\xc1\xd3\x20",                  "rcl ebx, 32"),
    (None, [REG.X86_64.OF], b"\xc1\xd3\x21",                  "rcl ebx, 33"),
    (None, [],              b"\xbb\x00\x00\x00\x80",          "mov ebx, 0x80000000"),
    (None, [],              b"\xd1\xd3",                      "rcl ebx, 1"),
    (None, [],              b"\xbb\x00\x00\x00\x80",          "mov ebx, 0x80000000"),
    (None, [REG.X86_64.OF], b"\xc1\xd3\x02",                  "rcl ebx, 2"),
    (None, [],              b"\xbb\x00\x00\x00\x80",          "mov ebx, 0x80000000"),
    (None, [REG.X86_64.OF], b"\xc1\xd3\x03",                  "rcl ebx, 3"),
    (None, [],              b"\xbb\x01\x00\x00\x00",          "mov ebx, 0x00000001"),
    (None, [],              b"\xd1\xd3",                      "rcl ebx, 1"),
    (None, [],              b"\xbb\x01\x00\x00\x00",          "mov ebx, 0x00000001"),
    (None, [REG.X86_64.OF], b"\xc1\xd3\x02",                  "rcl ebx, 2"),
    (None, [],              b"\xbb\x01\x00\x00\x00",          "mov ebx, 0x00000001"),
    (None, [REG.X86_64.OF], b"\xc1\xd3\x03",                  "rcl ebx, 3"),

    (None, [],              b"\xbb\xd5\x71\x36\x00",          "mov ebx, 0x3671d5"),
    (None, [],              b"\xf7\xdb",                      "neg ebx"),
    (None, [],              b"\xbb\x00\x00\x00\x80",          "mov ebx, 0x80000000"),
    (None, [],              b"\xf7\xdb",                      "neg ebx"),
    (None, [],              b"\xbb\x01\x00\x00\x80",          "mov ebx, 0x80000001"),
    (None, [],              b"\xf7\xdb",                      "neg ebx"),
    (None, [],              b"\xbb\x01\x00\x00\x00",          "mov ebx, 0x00000001"),
    (None, [],              b"\xf7\xdb",                      "neg ebx"),
    (None, [],              b"\xbb\xff\xff\xff\xff",          "mov ebx, 0xffffffff"),
    (None, [],              b"\xf7\xdb",                      "neg ebx"),
    (None, [],              b"\xbb\x00\x00\x00\x00",          "mov ebx, 0x00000000"),
    (None, [],              b"\xf7\xdb",                      "neg ebx"),

    (None, [],              b"\xbb\xd5\x71\x36\x00",          "mov ebx, 0x3671d5"),
    (None, [],              b"\xf7\xd3",                      "not ebx"),
    (None, [],              b"\xbb\x00\x00\x00\x80",          "mov ebx, 0x80000000"),
    (None, [],              b"\xf7\xd3",                      "not ebx"),
    (None, [],              b"\xbb\x01\x00\x00\x80",          "mov ebx, 0x80000001"),
    (None, [],              b"\xf7\xd3",                      "not ebx"),
    (None, [],              b"\xbb\x01\x00\x00\x00",          "mov ebx, 0x00000001"),
    (None, [],              b"\xf7\xd3",                      "not ebx"),
    (None, [],              b"\xbb\xff\xff\xff\xff",          "mov ebx, 0xffffffff"),
    (None, [],              b"\xf7\xd3",                      "not ebx"),
    (None, [],              b"\xbb\x00\x00\x00\x00",          "mov ebx, 0x00000000"),
    (None, [],              b"\xf7\xd3",                      "not ebx"),

    (None, [],              b"\xf9",                          "stc"),
    (None, [],              b"\xbb\xfe\xff\xff\xff",          "mov ebx, 0xfffffffe"),
    (None, [],              b"\xb8\x01\x00\x00\x00",          "mov eax, 0x00000001"),
    (None, [],              b"\x11\xd8",                      "adc eax, ebx"),

    (None, [],              b"\xf9",                          "stc"),
    (None, [],              b"\xbb\xfe\xff\xff\xff",          "mov ebx, 0xfffffffe"),
    (None, [],              b"\xb8\x02\x00\x00\x00",          "mov eax, 0x00000002"),
    (None, [],              b"\x11\xd8",                      "adc eax, ebx"),

    (None, [],              b"\xf9",                          "stc"),
    (None, [],              b"\x48\xc7\xc3\xff\xff\xff\xff",  "mov rbx, -1"),
    (None, [],              b"\x48\xc7\xc0\x01\x00\x00\x00",  "mov rax, 1"),
    (None, [],              b"\x48\x11\xc3",                  "adc rax, rbx"),

    (None, [],              b"\xf9",                          "stc"),
    (None, [],              b"\x48\xc7\xc3\xff\xff\xff\xff",  "mov rbx, -1"),
    (None, [],              b"\x48\xc7\xc0\x02\x00\x00\x00",  "mov rax, 2"),
    (None, [],              b"\x48\x11\xc3",                  "adc rax, rbx"),

    (None, [],              b"\xf8",                          "clc"),
    (None, [],              b"\x48\xc7\xc3\xff\xff\xff\xff",  "mov rbx, -1"),
    (None, [],              b"\x48\xc7\xc0\x02\x00\x00\x00",  "mov rax, 2"),
    (None, [],              b"\x48\x11\xc3",                  "adc rax, rbx"),

    (None, [],              b"\xf9",                                      "stc"),
    (None, [],              b"\x48\xbb\xff\xff\xff\xff\xff\xff\xff\x7f",  "mov rbx, 0x7fffffffffffffff"),
    (None, [],              b"\x48\xc7\xc0\x01\x00\x00\x00",              "mov rax, 1"),
    (None, [],              b"\x48\x11\xc3",                              "adc rax, rbx"),

    (None, [],              b"\xf9",                                      "stc"),
    (None, [],              b"\x48\xbb\xff\xff\xff\xff\xff\xff\xff\x7f",  "mov rbx, 0x7fffffffffffffff"),
    (None, [],              b"\x48\xc7\xc0\x00\x00\x00\x00",              "mov rax, 0"),
    (None, [],              b"\x48\x11\xc3",                              "adc rax, rbx"),

    (None, [],              b"\xf8",                                      "clc"),
    (None, [],              b"\x48\xbb\xff\xff\xff\xff\xff\xff\xff\x7f",  "mov rbx, 0x7fffffffffffffff"),
    (None, [],              b"\x48\xc7\xc0\x01\x00\x00\x00",              "mov rax, 1"),
    (None, [],              b"\x48\x11\xc3",                              "adc rax, rbx"),

    (None, [],              b"\xf8",                                      "clc"),
    (None, [],              b"\x48\xbb\xff\xff\xff\xff\xff\xff\xff\x7f",  "mov rbx, 0x7fffffffffffffff"),
    (None, [],              b"\x48\xc7\xc0\x02\x00\x00\x00",              "mov rax, 2"),
    (None, [],              b"\x48\x11\xc3",                              "adc rax, rbx"),

    (None, [],              b"\xf9",                                      "stc"),
    (None, [],              b"\x48\xbb\xff\xff\xff\xff\xff\xff\xff\x7f",  "mov rbx, 0x7fffffffffffffff"),
    (None, [],              b"\x48\xc7\xc0\x02\x00\x00\x00",              "mov rax, 2"),
    (None, [],              b"\x48\x11\xc3",                              "adc rax, rbx"),

    (None, [],              b"\xf9",                                      "stc"),
    (None, [],              b"\x48\xbb\xff\xfe\xff\xff\xff\xff\xff\x7f",  "mov rbx, 0x7ffffffffffffffe"),
    (None, [],              b"\x48\xc7\xc0\x01\x00\x00\x00",              "mov rax, 1"),
    (None, [],              b"\x48\x11\xc3",                              "adc rax, rbx"),
]


def emu_with_unicorn(opcode, istate):
    # Initialize emulator in x86_64 mode
    mu = Uc(UC_ARCH_X86, UC_MODE_64)

    # map memory for this emulation
    mu.mem_map(ADDR, SIZE)

    # write machine code to be emulated to memory
    index = 0
    for _, _, op, _ in CODE:
        mu.mem_write(ADDR+index, op)
        index += len(op)

    mu.mem_write(STACK,             bytes(istate['stack']))
    mu.mem_write(HEAP,              bytes(istate['heap']))
    mu.reg_write(UC_X86_REG_EFLAGS, istate['eflags'])
    mu.reg_write(UC_X86_REG_RAX,    istate['rax'])
    mu.reg_write(UC_X86_REG_RBX,    istate['rbx'])
    mu.reg_write(UC_X86_REG_RCX,    istate['rcx'])
    mu.reg_write(UC_X86_REG_RDX,    istate['rdx'])
    mu.reg_write(UC_X86_REG_RSI,    istate['rsi'])
    mu.reg_write(UC_X86_REG_RDI,    istate['rdi'])
    mu.reg_write(UC_X86_REG_RIP,    istate['rip'])
    mu.reg_write(UC_X86_REG_RSP,    istate['rsp'])
    mu.reg_write(UC_X86_REG_RBP,    istate['rbp'])
    mu.reg_write(UC_X86_REG_R8,     istate['r8'])
    mu.reg_write(UC_X86_REG_R9,     istate['r9'])
    mu.reg_write(UC_X86_REG_R10,    istate['r10'])
    mu.reg_write(UC_X86_REG_R11,    istate['r11'])
    mu.reg_write(UC_X86_REG_R12,    istate['r12'])
    mu.reg_write(UC_X86_REG_R13,    istate['r13'])
    mu.reg_write(UC_X86_REG_R14,    istate['r14'])
    mu.reg_write(UC_X86_REG_R15,    istate['r15'])
    mu.reg_write(UC_X86_REG_XMM0,   istate['xmm0'])
    mu.reg_write(UC_X86_REG_XMM1,   istate['xmm1'])
    mu.reg_write(UC_X86_REG_XMM2,   istate['xmm2'])
    mu.reg_write(UC_X86_REG_XMM3,   istate['xmm3'])
    mu.reg_write(UC_X86_REG_XMM4,   istate['xmm4'])
    mu.reg_write(UC_X86_REG_XMM5,   istate['xmm5'])
    mu.reg_write(UC_X86_REG_XMM6,   istate['xmm6'])
    mu.reg_write(UC_X86_REG_XMM7,   istate['xmm7'])
    mu.reg_write(UC_X86_REG_XMM8,   istate['xmm8'])
    mu.reg_write(UC_X86_REG_XMM9,   istate['xmm9'])
    mu.reg_write(UC_X86_REG_XMM10,  istate['xmm10'])
    mu.reg_write(UC_X86_REG_XMM11,  istate['xmm11'])
    mu.reg_write(UC_X86_REG_XMM12,  istate['xmm12'])
    mu.reg_write(UC_X86_REG_XMM13,  istate['xmm13'])
    mu.reg_write(UC_X86_REG_XMM14,  istate['xmm14'])
    mu.reg_write(UC_X86_REG_XMM15,  istate['xmm15'])
    mu.reg_write(UC_X86_REG_MM0,    istate['mm0'])
    mu.reg_write(UC_X86_REG_MM1,    istate['mm1'])
    mu.reg_write(UC_X86_REG_MM2,    istate['mm2'])
    mu.reg_write(UC_X86_REG_MM3,    istate['mm3'])
    mu.reg_write(UC_X86_REG_MM4,    istate['mm4'])
    mu.reg_write(UC_X86_REG_MM5,    istate['mm5'])
    mu.reg_write(UC_X86_REG_MM6,    istate['mm6'])
    mu.reg_write(UC_X86_REG_MM7,    istate['mm7'])
    mu.reg_write(UC_X86_REG_MXCSR,  istate['mxcsr'])
    mu.reg_write(UC_X86_REG_FPCW,   istate['fcw'])
    mu.reg_write(UC_X86_REG_FPSW,   istate['fsw'])
    mu.reg_write(UC_X86_REG_FPTAG,  istate['ftw'])

    # emulate code in infinite time & unlimited instructions
    mu.emu_start(istate['rip'], istate['rip'] + len(opcode))

    ostate = {
        "stack":        mu.mem_read(STACK, 0x200),
        "heap":         mu.mem_read(HEAP, 0x200),
        "eflags":       mu.reg_read(UC_X86_REG_EFLAGS),
        "rax":          mu.reg_read(UC_X86_REG_RAX),
        "rbx":          mu.reg_read(UC_X86_REG_RBX),
        "rcx":          mu.reg_read(UC_X86_REG_RCX),
        "rdx":          mu.reg_read(UC_X86_REG_RDX),
        "rsi":          mu.reg_read(UC_X86_REG_RSI),
        "rdi":          mu.reg_read(UC_X86_REG_RDI),
        "rip":          mu.reg_read(UC_X86_REG_RIP),
        "rsp":          mu.reg_read(UC_X86_REG_RSP),
        "rbp":          mu.reg_read(UC_X86_REG_RBP),
        "r8":           mu.reg_read(UC_X86_REG_R8),
        "r9":           mu.reg_read(UC_X86_REG_R9),
        "r10":          mu.reg_read(UC_X86_REG_R10),
        "r11":          mu.reg_read(UC_X86_REG_R11),
        "r12":          mu.reg_read(UC_X86_REG_R12),
        "r13":          mu.reg_read(UC_X86_REG_R13),
        "r14":          mu.reg_read(UC_X86_REG_R14),
        "r15":          mu.reg_read(UC_X86_REG_R15),
        "xmm0":         mu.reg_read(UC_X86_REG_XMM0),
        "xmm1":         mu.reg_read(UC_X86_REG_XMM1),
        "xmm2":         mu.reg_read(UC_X86_REG_XMM2),
        "xmm3":         mu.reg_read(UC_X86_REG_XMM3),
        "xmm4":         mu.reg_read(UC_X86_REG_XMM4),
        "xmm5":         mu.reg_read(UC_X86_REG_XMM5),
        "xmm6":         mu.reg_read(UC_X86_REG_XMM6),
        "xmm7":         mu.reg_read(UC_X86_REG_XMM7),
        "xmm8":         mu.reg_read(UC_X86_REG_XMM8),
        "xmm9":         mu.reg_read(UC_X86_REG_XMM9),
        "xmm10":        mu.reg_read(UC_X86_REG_XMM10),
        "xmm11":        mu.reg_read(UC_X86_REG_XMM11),
        "xmm12":        mu.reg_read(UC_X86_REG_XMM12),
        "xmm13":        mu.reg_read(UC_X86_REG_XMM13),
        "xmm14":        mu.reg_read(UC_X86_REG_XMM14),
        "xmm15":        mu.reg_read(UC_X86_REG_XMM15),
        "mm0":          mu.reg_read(UC_X86_REG_MM0),
        "mm1":          mu.reg_read(UC_X86_REG_MM1),
        "mm2":          mu.reg_read(UC_X86_REG_MM2),
        "mm3":          mu.reg_read(UC_X86_REG_MM3),
        "mm4":          mu.reg_read(UC_X86_REG_MM4),
        "mm5":          mu.reg_read(UC_X86_REG_MM5),
        "mm6":          mu.reg_read(UC_X86_REG_MM6),
        "mm7":          mu.reg_read(UC_X86_REG_MM7),
        "mxcsr":        mu.reg_read(UC_X86_REG_MXCSR),
        "mxcsr_mask":   0xFFBF,  # Unsupported by Unicorn
        "fcw":          mu.reg_read(UC_X86_REG_FPCW),
        "fsw":          mu.reg_read(UC_X86_REG_FPSW),
        "ftw":          mu.reg_read(UC_X86_REG_FPTAG),
    }
    return ostate


def emu_with_triton(opcode, istate):
    ctx = TritonContext()
    ctx.setArchitecture(ARCH.X86_64)

    inst = Instruction(opcode)
    inst.setAddress(istate['rip'])

    ctx.setConcreteMemoryAreaValue(STACK,                    bytes(istate['stack']))
    ctx.setConcreteMemoryAreaValue(HEAP,                     bytes(istate['heap']))
    ctx.setConcreteRegisterValue(ctx.registers.eflags,       istate['eflags'])
    ctx.setConcreteRegisterValue(ctx.registers.rax,          istate['rax'])
    ctx.setConcreteRegisterValue(ctx.registers.rbx,          istate['rbx'])
    ctx.setConcreteRegisterValue(ctx.registers.rcx,          istate['rcx'])
    ctx.setConcreteRegisterValue(ctx.registers.rdx,          istate['rdx'])
    ctx.setConcreteRegisterValue(ctx.registers.rsi,          istate['rsi'])
    ctx.setConcreteRegisterValue(ctx.registers.rdi,          istate['rdi'])
    ctx.setConcreteRegisterValue(ctx.registers.rip,          istate['rip'])
    ctx.setConcreteRegisterValue(ctx.registers.rsp,          istate['rsp'])
    ctx.setConcreteRegisterValue(ctx.registers.rbp,          istate['rbp'])
    ctx.setConcreteRegisterValue(ctx.registers.r8,           istate['r8'])
    ctx.setConcreteRegisterValue(ctx.registers.r9,           istate['r9'])
    ctx.setConcreteRegisterValue(ctx.registers.r10,          istate['r10'])
    ctx.setConcreteRegisterValue(ctx.registers.r11,          istate['r11'])
    ctx.setConcreteRegisterValue(ctx.registers.r12,          istate['r12'])
    ctx.setConcreteRegisterValue(ctx.registers.r13,          istate['r13'])
    ctx.setConcreteRegisterValue(ctx.registers.r14,          istate['r14'])
    ctx.setConcreteRegisterValue(ctx.registers.r15,          istate['r15'])
    ctx.setConcreteRegisterValue(ctx.registers.xmm0,         istate['xmm0'])
    ctx.setConcreteRegisterValue(ctx.registers.xmm1,         istate['xmm1'])
    ctx.setConcreteRegisterValue(ctx.registers.xmm2,         istate['xmm2'])
    ctx.setConcreteRegisterValue(ctx.registers.xmm3,         istate['xmm3'])
    ctx.setConcreteRegisterValue(ctx.registers.xmm4,         istate['xmm4'])
    ctx.setConcreteRegisterValue(ctx.registers.xmm5,         istate['xmm5'])
    ctx.setConcreteRegisterValue(ctx.registers.xmm6,         istate['xmm6'])
    ctx.setConcreteRegisterValue(ctx.registers.xmm7,         istate['xmm7'])
    ctx.setConcreteRegisterValue(ctx.registers.xmm8,         istate['xmm8'])
    ctx.setConcreteRegisterValue(ctx.registers.xmm9,         istate['xmm9'])
    ctx.setConcreteRegisterValue(ctx.registers.xmm10,        istate['xmm10'])
    ctx.setConcreteRegisterValue(ctx.registers.xmm11,        istate['xmm11'])
    ctx.setConcreteRegisterValue(ctx.registers.xmm12,        istate['xmm12'])
    ctx.setConcreteRegisterValue(ctx.registers.xmm13,        istate['xmm13'])
    ctx.setConcreteRegisterValue(ctx.registers.xmm14,        istate['xmm14'])
    ctx.setConcreteRegisterValue(ctx.registers.xmm15,        istate['xmm15'])
    ctx.setConcreteRegisterValue(ctx.registers.mm0,          istate['mm0'])
    ctx.setConcreteRegisterValue(ctx.registers.mm1,          istate['mm1'])
    ctx.setConcreteRegisterValue(ctx.registers.mm2,          istate['mm2'])
    ctx.setConcreteRegisterValue(ctx.registers.mm3,          istate['mm3'])
    ctx.setConcreteRegisterValue(ctx.registers.mm4,          istate['mm4'])
    ctx.setConcreteRegisterValue(ctx.registers.mm5,          istate['mm5'])
    ctx.setConcreteRegisterValue(ctx.registers.mm6,          istate['mm6'])
    ctx.setConcreteRegisterValue(ctx.registers.mm7,          istate['mm7'])
    ctx.setConcreteRegisterValue(ctx.registers.mxcsr,        istate['mxcsr'])
    ctx.setConcreteRegisterValue(ctx.registers.mxcsr_mask,   istate['mxcsr_mask'])
    ctx.setConcreteRegisterValue(ctx.registers.fcw,          istate['fcw'])
    ctx.setConcreteRegisterValue(ctx.registers.fsw,          istate['fsw'])
    ctx.setConcreteRegisterValue(ctx.registers.ftw,          istate['ftw'])

    ctx.processing(inst)
    # print(inst)
    # for se in inst.getSymbolicExpressions():
    #    print(se)

    ostate = {
        "stack":       ctx.getConcreteMemoryAreaValue(STACK, 0x200),
        "heap":        ctx.getConcreteMemoryAreaValue(HEAP, 0x200),
        "eflags":      ctx.getConcreteRegisterValue(ctx.registers.eflags),
        "rax":         ctx.getSymbolicRegisterValue(ctx.registers.rax),
        "rbx":         ctx.getSymbolicRegisterValue(ctx.registers.rbx),
        "rcx":         ctx.getSymbolicRegisterValue(ctx.registers.rcx),
        "rdx":         ctx.getSymbolicRegisterValue(ctx.registers.rdx),
        "rsi":         ctx.getSymbolicRegisterValue(ctx.registers.rsi),
        "rdi":         ctx.getSymbolicRegisterValue(ctx.registers.rdi),
        "rip":         ctx.getSymbolicRegisterValue(ctx.registers.rip),
        "rsp":         ctx.getSymbolicRegisterValue(ctx.registers.rsp),
        "rbp":         ctx.getSymbolicRegisterValue(ctx.registers.rbp),
        "r8":          ctx.getSymbolicRegisterValue(ctx.registers.r8),
        "r9":          ctx.getSymbolicRegisterValue(ctx.registers.r9),
        "r10":         ctx.getSymbolicRegisterValue(ctx.registers.r10),
        "r11":         ctx.getSymbolicRegisterValue(ctx.registers.r11),
        "r12":         ctx.getSymbolicRegisterValue(ctx.registers.r12),
        "r13":         ctx.getSymbolicRegisterValue(ctx.registers.r13),
        "r14":         ctx.getSymbolicRegisterValue(ctx.registers.r14),
        "r15":         ctx.getSymbolicRegisterValue(ctx.registers.r15),
        "xmm0":        ctx.getSymbolicRegisterValue(ctx.registers.xmm0),
        "xmm1":        ctx.getSymbolicRegisterValue(ctx.registers.xmm1),
        "xmm2":        ctx.getSymbolicRegisterValue(ctx.registers.xmm2),
        "xmm3":        ctx.getSymbolicRegisterValue(ctx.registers.xmm3),
        "xmm4":        ctx.getSymbolicRegisterValue(ctx.registers.xmm4),
        "xmm5":        ctx.getSymbolicRegisterValue(ctx.registers.xmm5),
        "xmm6":        ctx.getSymbolicRegisterValue(ctx.registers.xmm6),
        "xmm7":        ctx.getSymbolicRegisterValue(ctx.registers.xmm7),
        "xmm8":        ctx.getSymbolicRegisterValue(ctx.registers.xmm8),
        "xmm9":        ctx.getSymbolicRegisterValue(ctx.registers.xmm9),
        "xmm10":       ctx.getSymbolicRegisterValue(ctx.registers.xmm10),
        "xmm11":       ctx.getSymbolicRegisterValue(ctx.registers.xmm11),
        "xmm12":       ctx.getSymbolicRegisterValue(ctx.registers.xmm12),
        "xmm13":       ctx.getSymbolicRegisterValue(ctx.registers.xmm13),
        "xmm14":       ctx.getSymbolicRegisterValue(ctx.registers.xmm14),
        "xmm15":       ctx.getSymbolicRegisterValue(ctx.registers.xmm15),
        "mm0":         ctx.getSymbolicRegisterValue(ctx.registers.mm0),
        "mm1":         ctx.getSymbolicRegisterValue(ctx.registers.mm1),
        "mm2":         ctx.getSymbolicRegisterValue(ctx.registers.mm2),
        "mm3":         ctx.getSymbolicRegisterValue(ctx.registers.mm3),
        "mm4":         ctx.getSymbolicRegisterValue(ctx.registers.mm4),
        "mm5":         ctx.getSymbolicRegisterValue(ctx.registers.mm5),
        "mm6":         ctx.getSymbolicRegisterValue(ctx.registers.mm6),
        "mm7":         ctx.getSymbolicRegisterValue(ctx.registers.mm7),
        "mxcsr":       ctx.getSymbolicRegisterValue(ctx.registers.mxcsr),
        "mxcsr_mask":  ctx.getSymbolicRegisterValue(ctx.registers.mxcsr_mask),
        "fcw":         ctx.getSymbolicRegisterValue(ctx.registers.fcw),
        "fsw":         ctx.getSymbolicRegisterValue(ctx.registers.fsw),
        "ftw":         ctx.getSymbolicRegisterValue(ctx.registers.ftw),

    }
    return ostate


def diff_state(state1, state2):
    for k, v in list(state1.items()):
        if (k == 'heap' or k == 'stack') and v != state2[k]:
            print('\t%s: (UC) != (TT)' %(k))
        elif not (k == 'heap' or k == 'stack') and v != state2[k]:
            print('\t%s: %#x (UC) != %#x (TT)' %(k, v, state2[k]))
    return


def dump_state(state):
    # Stack dump (16-byte boundary)
    print("stack:")
    for i, b in enumerate(state['stack']):
        if (i % 16) == 0:
            print("")
        print("%02X " % b, end='')
    print("\n")
    # Heap dump (16-byte boundary)
    print("heap:")
    for i, b in enumerate(state['heap']):
        if (i % 16) == 0:
            print("")
        print("%02X " % b, end='')
    print("\n")
    # EFLAGS register
    print("eflags: 0x%X" % state['eflags'])
    # GP registers
    print("rax: 0x%X" % state['rax'])
    print("rbx: 0x%X" % state['rbx'])
    print("rcx: 0x%X" % state['rcx'])
    print("rdx: 0x%X" % state['rdx'])
    print("rsi: 0x%X" % state['rsi'])
    print("rdi: 0x%X" % state['rdi'])
    print("rip: 0x%X" % state['rip'])
    print("rsp: 0x%X" % state['rsp'])
    print("rbp: 0x%X" % state['rbp'])
    print("r8: 0x%X" % state['r8'])
    print("r9: 0x%X" % state['r9'])
    print("r10: 0x%X" % state['r10'])
    print("r11: 0x%X" % state['r11'])
    print("r12: 0x%X" % state['r12'])
    print("r13: 0x%X" % state['r13'])
    print("r14: 0x%X" % state['r14'])
    print("r15: 0x%X" % state['r15'])
    # XMM registers
    print("xmm0: 0x%X" % state['xmm0'])
    print("xmm1: 0x%X" % state['xmm1'])
    print("xmm2: 0x%X" % state['xmm2'])
    print("xmm3: 0x%X" % state['xmm3'])
    print("xmm4: 0x%X" % state['xmm4'])
    print("xmm5: 0x%X" % state['xmm5'])
    print("xmm6: 0x%X" % state['xmm6'])
    print("xmm7: 0x%X" % state['xmm7'])
    print("xmm8: 0x%X" % state['xmm8'])
    print("xmm9: 0x%X" % state['xmm9'])
    print("xmm10: 0x%X" % state['xmm10'])
    print("xmm11: 0x%X" % state['xmm11'])
    print("xmm12: 0x%X" % state['xmm12'])
    print("xmm13: 0x%X" % state['xmm13'])
    print("xmm14: 0x%X" % state['xmm14'])
    print("xmm15: 0x%X" % state['xmm15'])
    # MMX registers
    print("mm0: 0x%X" % state['mm0'])
    print("mm1: 0x%X" % state['mm1'])
    print("mm2: 0x%X" % state['mm2'])
    print("mm3: 0x%X" % state['mm3'])
    print("mm4: 0x%X" % state['mm4'])
    print("mm5: 0x%X" % state['mm5'])
    print("mm6: 0x%X" % state['mm6'])
    print("mm7: 0x%X" % state['mm7'])
    # SSE and x87 FPU registers
    print("mxcsr: 0x%X" % state['mxcsr'])
    print("mxcsr_mask: 0x%X" % state['mxcsr_mask'])
    print("fcw: 0x%X" % state['fcw'])
    print("fsw: 0x%X" % state['fsw'])
    print("ftw: 0x%X" % state['ftw'])


if __name__ == '__main__':
    # initial state
    state = {
        "stack":      bytearray(b"".join([pack('B', 0) for i in range(512)])),
        "heap":       bytearray(b"".join([pack('B', i) for i in range(256)])),
        "eflags":     2, # bit 2 is always 1
        "rax":        0,
        "rbx":        0,
        "rcx":        0,
        "rdx":        0,
        "rsi":        0,
        "rdi":        0,
        "rip":        ADDR,
        "rsp":        STACK,
        "rbp":        STACK,
        "r8":         0,
        "r9":         0,
        "r10":        0,
        "r11":        0,
        "r12":        0,
        "r13":        0,
        "r14":        0,
        "r15":        0,
        "xmm0":       0x0,
        "xmm1":       0x0,
        "xmm2":       0x0,
        "xmm3":       0x0,
        "xmm4":       0x0,
        "xmm5":       0x0,
        "xmm6":       0x0,
        "xmm7":       0x0,
        "xmm8":       0x0,
        "xmm9":       0x0,
        "xmm10":      0x0,
        "xmm11":      0x0,
        "xmm12":      0x0,
        "xmm13":      0x0,
        "xmm14":      0x0,
        "xmm15":      0x0,
        "mm0":        0x0,      # Unsupported by Unicorn
        "mm1":        0x0,      # Unsupported by Unicorn
        "mm2":        0x0,      # Unsupported by Unicorn
        "mm3":        0x0,      # Unsupported by Unicorn
        "mm4":        0x0,      # Unsupported by Unicorn
        "mm5":        0x0,      # Unsupported by Unicorn
        "mm6":        0x0,      # Unsupported by Unicorn
        "mm7":        0x0,      # Unsupported by Unicorn
        "mxcsr":      0x1F80,   # Default value at program start
        "mxcsr_mask": 0xFFBF,   # Default value at program start
        "fcw":        0x027F,   # Default value at program start
        "fsw":        0x0000,   # Default value at program start
        "ftw":        0x5555    # Default value at program start
    }

    for st, undef, opcode, disassembly in CODE:
        if st is not None:
            state.update(st)
        try:
            #print("> Unicorn emulation: %s" % disassembly)
            uc_state = emu_with_unicorn(opcode, state)
            #print("> Triton emulation: %s" % disassembly)
            tt_state = emu_with_triton(opcode, state)
            #print("> Emulation done")
        except Exception as e:
            print('[KO] %s' %(disassembly))
            print('\t%s' %(e))
            sys.exit(-1)

        # We ignore flags that are tagged as undef.
        # To do that we set them in both TT and UC state.
        for reg in undef:
            if reg == REG.X86_64.OF:
                uc_state['eflags'] = uc_state['eflags'] | 0x0800
                tt_state['eflags'] = tt_state['eflags'] | 0x0800

        if uc_state != tt_state:
            print('[KO] %s' %(disassembly))
            #dump_state(uc_state)
            #dump_state(tt_state)
            diff_state(uc_state, tt_state)
            sys.exit(-1)

        print('[OK] %s' %(disassembly))
        state = tt_state

    sys.exit(0)
