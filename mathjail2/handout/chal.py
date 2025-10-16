#!/usr/local/bin/python3
from typing import Callable, Iterator, Tuple
from hashlib import sha256
import random


class MathJailError(Exception):
    pass


class MathJail:
    title: str
    description: str

    def __init__(self, max_size: int):
        self.max_size = max_size

    def run(self, code: str) -> bool:
        func = self.validate(code)
        for input, output in self.gen_test_cases():
            user_output = func(input)
            if not isinstance(user_output, int) or user_output != output:
                return False
        return True

    def gen_test_cases(self) -> Iterator[Tuple[int, int]]:
        raise NotImplementedError

    def validate(self, code: str) -> Callable[[int], int]:
        if len(code) > self.max_size:
            raise MathJailError(f'Code is too large ({len(code)} > {self.max_size})')

        for c in code:
            if c not in '0123456789n+-*/%^&|<~>()':
                raise MathJailError(f'Illegal character: {c!r}')

        try:
            func = eval(f'lambda n: {code}', {}, {})
        except Exception as e:
            raise MathJailError(f'Could not compile expression: {e}')
        return func

    def __repr__(self):
        return self.description


class SHA256Jail(MathJail):
    title = 'SHA-256'
    description = 'Write an expression that takes a 64-byte string\n' \
                  'and outputs its SHA-256 hash (in big-endian).\n'

    def gen_test_cases(self):
        random.seed(0x1337)
        for _ in range(256):
            s = random.randbytes(64)
            n = int.from_bytes(s, 'big')
            output = int.from_bytes(sha256(s).digest(), 'big')
            yield (n, output)


if __name__ == '__main__':
    print('You thought you escaped, but the Warden has one last trick. The exit is sealed by a lock\n'
          'that only answers to SHA-256. One level, one shot - hash your way to freedom.\n')

    jail = SHA256Jail(19850)
    print(f'Level X: {jail.title}')
    print('-' * 30)
    print(jail)

    code = input(f'Enter your expression ({jail.max_size} characters max): ')

    try:
        result = jail.run(code)
    except Exception as e:
        print(e)
        exit(1)

    if not result:
        print('You have failed.')
        exit(1)

    with open('flag.txt', 'r') as f:
        print(f"Your victory is well-deserved: {f.read()}")

