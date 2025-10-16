#!/usr/bin/python3
from subprocess import Popen
from time import sleep
import tempfile

proc = Popen(['/usr/bin/sage'], stdin=-1)
print('sagemath may take some time to start up. wait until the "sage:" prompt appears before inputting your payload')
inp = input('')[:400]
if any(c not in '# abcdefghijklmnopqrstuvwxyz;")._' for c in inp):
    print('bad')
    exit(1)
proc.stdin.write(f'globals().clear();__builtins__={{}};\n{inp};\n'.encode())
proc.stdin.flush()
sleep(1.0)
