#!/usr/local/bin/python3 -u
from RestrictedPython import compile_restricted, safe_globals

# we love when our users write beautiful typed code :D
from typing import NamedTuple, TypedDict

exec_globals = {
    **safe_globals,
    'NamedTuple': NamedTuple,
    'TypedDict': TypedDict,

    # globals needed to create classes with RestrictedPython
    '__name__': '<string>',
    '__metaclass__': type
}
exec_loc = {}

code = ""
print("Give me beautiful but safe code:")
while (line := input()) != "# EOF":
    code += line + "\n"

code = compile_restricted(code, '<string>', 'exec')
exec(code, exec_globals, exec_loc)
