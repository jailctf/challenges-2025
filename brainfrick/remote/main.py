#!/usr/local/bin/python3
from bfi import interpret
from subprocess import check_output

def bf_eval(code: str) -> str:
    return interpret(code, input_data='', buffer_output=True)

def py_eval(code: str) -> str:
    return str(eval(code))

def js_eval(code: str) -> str:
    return check_output(['node', '-p', code], text=True).strip()

code = input('> ')

if any(c not in '<>-+.,[]' for c in code):
    print('bf only pls')
    exit()

if bf_eval(code) == py_eval(code) == js_eval(code):
    print(open('flag.txt', 'r').read())
