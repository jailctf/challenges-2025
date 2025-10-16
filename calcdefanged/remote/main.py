#!/usr/local/bin/python3
from sys import addaudithook
from os import _exit
from re import match


def safe_eval(exit, code):
    def hook(*a):
        exit(0)
    def disabled_exit(*a):
        pass

    def dummy():
        pass

    dummy.__code__ = compile(code, "<code>", "eval")
    print("Activating audit hook...")
    addaudithook(hook)
    val = dummy()
    # audit hooks do not allow me to do important stuff afterwards, so i am disabling this one after eval completion
    # surely this won't have unintended effects down the line, ... right?
    print("Disabling audit hook...")
    exit = disabled_exit
    return val


if __name__ == "__main__":
    expr = input("Math expression: ")

    if len(expr) <= 200 and match(r"[0-9+\-*/]+", expr):
        # extra constraints just to make sure people don't use signal this time ...
        if len(expr) <= 75 and ' ' not in expr and '_' not in expr:
            print(safe_eval(_exit, expr))
        else:
            print('Unacceptable')
    else:
        print("Do you know what is a calculator?")
