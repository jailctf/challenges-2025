#!/usr/bin/env python3
import os
import sys
import base64
import tempfile

from asm_runner import AsmRunner
from cs_runner import CsRunner
from scm_runner import ScmRunner
from js_runner import JsRunner
from bash_runner import BashRunner

FLAG = os.getenv("FLAG")

if FLAG is None:
    print("Unable to load flag, contact an admin.")
    sys.exit(1)

def print_header():
    """Print the challenge banner"""
    print("=" * 50)
    print("|        Welcome to Polyglotquine 5equel!        |")
    print("|" + " " * 48 + "|")
    print("| The goal is simple, write a polyglot program   |")
    print("| that prints its own source code in the         |")
    print("| following 5 languages:                         |")
    print("| " + "-" * 46 + " |")
    print("|     x64 Assembly | Bash | C# | JS | Scheme     |")
    print("| " + "-" * 46 + " |")
    print("| Nothing too crazy... Good luck!                |")
    print("=" * 50)
    print()


def main():
    print_header()

    sys.stdout.write("Base64 encoded code > ")
    sys.stdout.flush()
    input_str = sys.stdin.readline().strip()

    # Decode base64
    try:
        code = base64.b64decode(input_str)
    except Exception:
        print("Failed to decode Base64 input")
        return 1

    if len(code) <= 5:
        print("Code length must be greater than 5")
        return 1
    
    print("Starting... (May take a bit to fully run)")

    # Create temp directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create all runners
        runners = [
            AsmRunner(code, temp_dir),
            CsRunner(code, temp_dir),
            ScmRunner(code, temp_dir),
            JsRunner(code, temp_dir),
            BashRunner(code, temp_dir),
        ]
        
        # Compile and run each language
        for runner in runners:
            # Compile if needed
            if not runner.compile():
                print("You lose!")
                return 1

            # Run and check
            if not runner.run():
                print("You lose!")
                return 1

            # Cleanup
            runner.cleanup()

        # All tests passed!
        print(f"You win! {FLAG}")
        return 0


if __name__ == '__main__':
    sys.exit(main())
