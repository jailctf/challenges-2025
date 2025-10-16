#!/usr/local/bin/python3
import modelscan.settings
import modelscan.modelscan
import pickle

scan = modelscan.modelscan.ModelScan(settings=modelscan.settings.DEFAULT_SETTINGS)

open('/tmp/malicious.pkl', 'wb').write(bytes.fromhex(input('> '))[:23])

result = scan.scan('/tmp/malicious.pkl')
if result['issues'] or result['errors']:
    print('no')
    exit()

pickle.loads(open('/tmp/malicious.pkl', 'rb').read())

