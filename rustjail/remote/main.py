#!/usr/bin/python3
import string
import os

allowed = set(string.ascii_lowercase+string.digits+' :._(){}"')

os.environ['RUSTUP_HOME']='/usr/local/rustup'
os.environ['CARGO_HOME']='/usr/local/cargo'
os.environ['PATH']='/usr/local/cargo/bin:/usr/bin'

inp = input("gib cod: ").strip()
if not allowed.issuperset(set(inp)):
    print("bad cod")
    exit()
with open("/tmp/cod.rs", "w") as f:
    f.write(inp)
os.system("/usr/local/cargo/bin/rustc /tmp/cod.rs -o /tmp/cod")
os.system("/tmp/cod; echo Exited with status $?")
