#!/usr/local/bin/python3
from os import system

def immutable(cls: type):
    import ctypes
    TP_FLAGS_OFFSET = 21 * tuple.__itemsize__
    Py_TPFLAGS_IMMUTABLETYPE = 1 << 8

    view = ctypes.cast(id(cls) + TP_FLAGS_OFFSET, ctypes.POINTER(ctypes.c_ulong))
    view.contents.value |= Py_TPFLAGS_IMMUTABLETYPE
    assert cls.__flags__ & Py_TPFLAGS_IMMUTABLETYPE != 0

    return cls

@immutable
class SafeBuiltins[system]:
    __slots__ = ()
    __freebie__ = "What's a red herring?"

BANNED = "()[]:='\""

code = input("code: ")

for c in code:
    if c in BANNED:
        print("nope", repr(c))
        exit(1)

eval(code, {'__builtins__': SafeBuiltins()}, {})

