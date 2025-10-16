#!/usr/local/bin/python3
import os
import tempfile

inp = [int(n_str) for n_str in input('moon input > ').split()]

if not all(n > 255 for n in inp):
    print('bad input')
    exit()

with tempfile.NamedTemporaryFile(mode='w', suffix='.☾', delete_on_close=False) as f:
    f.write('print("loaded");' + ''.join([chr(n) for n in inp]))
    f.close()
    print('loading')
    os.system(f'☾ {f.name}')
    print('done')

