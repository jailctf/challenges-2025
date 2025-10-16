#!/usr/local/bin/python3 -u
import os
import subprocess
import tempfile
import re

print("go ham or go home")
code = input("> ")

if not re.fullmatch(r'[a-z *;_]+', code):
    print("u bad")
    exit(1)

with tempfile.TemporaryDirectory() as td:
    src_path = os.path.join(td, "source.cpp")
    compiled_path = os.path.join(td, "compiled")
    with open(src_path, "w") as file:
        file.write('int main() {\n' + code + '\n}\n')
   
    returncode = subprocess.call(["g++", "-B/usr/bin", "-o", compiled_path, src_path], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    if returncode != 0:
        print("Oops, there were some compilation errors!")
        exit(1)

    print("lets do it")
    subprocess.call([compiled_path])
    print('it is done')
