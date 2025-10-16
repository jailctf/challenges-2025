#!/usr/local/bin/python3
import re

isPrime = lambda num: num > 1 and all(num % i != 0 for i in range(2, num))

code = input("Prime Code > ")

if len(code) > 200 or not code.isascii() or "eta" in code:
    print("Relax")
    exit()

for m in re.finditer(r"\w+", code):
    if not isPrime(len(m.group(0))):
        print("Nope")
        exit()

eval(code, {'__builtins__': {}})
