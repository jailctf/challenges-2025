#!/usr/local/bin/python3

import sys
from os import _exit

sm = sys.monitoring
sm.use_tool_id(2, 'computer-monitor')

inp = input('> ')
code = compile(inp, '<string>', 'exec')

exit_hook = lambda *a: _exit(0)
sm.set_local_events(2, code, sm.events.BRANCH + sm.events.CALL)
sm.register_callback(2, sm.events.BRANCH, exit_hook)
sm.register_callback(2, sm.events.CALL, exit_hook)
exec(code, {}, {})

