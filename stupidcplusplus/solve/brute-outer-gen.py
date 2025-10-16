from os import system

for j in range(1, 6):
    for i in range(30,170):
        system(f'python3 gen.py {i}')

