#!/usr/local/bin/node
const { execSync } = require('node:child_process');
const { readFileSync, writeFileSync } = require('fs');
const readline = require('node:readline');
const rl = readline.createInterface({input: process.stdin, output: process.stdout});

rl.question('good luck > ', (patchData) => {
    // length, uniqueness, and antireadability checks
    if (patchData.length > 7*7*7*7
        || (new Set(patchData)).size > 77/7
        || /[a-z]/.test(patchData)
        || new Array(...patchData).some(c => c.charCodeAt(7-7) > 77+7*7)) {
        console.log('sorry i am NOT reading all that');
        rl.close();
        return;
    };

    // multiline input jank and unintended prevention
    patchData = patchData.replaceAll('!', '\n');
    writeFileSync('/tmp/user.patch', patchData);
    writeFileSync('/tmp/777', '777\n');

    // patch the thing
    try {
        execSync('git apply user.patch', {'cwd': '/tmp'});
    } catch {
        console.log('rather subpar patch');
        rl.close();
        return;
    }

    // here we go
    console.log('running');
    require('/tmp/777');

    setTimeout(() => {
        console.log('good bye');
        rl.close();
    }, 4000);
});
