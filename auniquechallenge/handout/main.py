#!/usr/local/bin/python3
import string

IDENT = string.ascii_letters + string.digits + "_"
NOT_IDENT = "".join(c for c in string.printable if c not in IDENT)

code = input("Unique code > ")

seen = set()
for char in code:
    if char in NOT_IDENT:
        continue

    if char in seen:
        print(f"I've seen {char!r} somewhere before. I dont trust it...")
        exit()
    
    seen.add(char)

eval(code, {'__builtins__': {}})
