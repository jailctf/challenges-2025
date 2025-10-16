#!/usr/local/bin/python3
import secrets
import random
from lottery_machine import flag

x = [*"%&()*,./:;>[]^{|}~"] # i deleted a bunch of characters because i just dislike them for being too cool.
random.shuffle(x)
charset = x[:4]
print(f'your lucky numbers are: {", ".join([str(ord(i)) for i in charset])}')
charset += ["_"]
count = 0

try:
    while count < 100:
        _ = secrets.token_bytes(128)
        secret = _
        for z in range(1025):
            code = input("cmd: ")
            if code == "submit":
                if input("lottery numbers? ") == secret.hex():
                    count += 1
                else:
                    raise ValueError("the winning ticket was " + secret.hex())
            elif any(i not in charset for i in code):
                raise ValueError("invalid cmd")
            else:
                try:
                    eval(code)
                except:
                    print("answering machine broke.")
except Exception as err:
    print(err)
if count == 100:
    print(f"you won! here is {flag:}")
else:
    print("better luck next time!")
